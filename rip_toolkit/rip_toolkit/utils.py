import os
import re
from datetime import datetime
from netCDF4 import Dataset
from pathlib import Path


def _parse_wrf_datetime(value: str) -> datetime:
    """Parse common WRF time string formats."""
    value = value.strip()
    for fmt in ("%Y-%m-%d_%H:%M:%S", "%Y-%m-%d_%H:%M", "%Y-%m-%d_%H"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unsupported WRF time format: {value}")


def _times_from_file(path: str) -> list[datetime]:
    """
    Read all frame times from a wrfout NetCDF file (Times variable).
    Falls back to parsing the timestamp from filename if Times is missing.
    """
    out = []
    with Dataset(path) as ds:
        if "Times" in ds.variables:
            times_var = ds.variables["Times"][:]  # typically shape (Time, DateStrLen)
            for row in times_var:
                # row is usually a char array; bytes decode handles this robustly
                tstr = (
                    row.tobytes()
                    .decode("ascii", errors="ignore")
                    .strip("\x00 ")
                    .strip()
                )
                if tstr:
                    out.append(_parse_wrf_datetime(tstr))
        else:
            # fallback: parse from filename suffix
            fname = os.path.basename(path)
            out.append(_parse_wrf_datetime(fname[-19:]))

    return out


def get_model_times(wrfout_dir: str) -> dict[float, str]:
    """
    Return available model times (hours since simulation start) mapped to date strings.

    Inputs:
    - wrfout_dir (str): Directory containing wrfout_* files.

    Outputs:
    - dict[float, str]: {model_hour: "YYYY-MM-DD_HH:MM:SS"} for all available frames.
    """
    if not os.path.isdir(wrfout_dir):
        raise FileNotFoundError(f"wrfout_dir does not exist: {wrfout_dir}")

    wrf_files = sorted(
        os.path.join(wrfout_dir, f)
        for f in os.listdir(wrfout_dir)
        if f.startswith("wrfout_")
    )
    if not wrf_files:
        raise ValueError(f"No files starting with 'wrfout_' found in: {wrfout_dir}")

    frame_datetimes = []
    for path in wrf_files:
        frame_datetimes.extend(_times_from_file(path))

    # deduplicate and sort in case times overlap across files
    frame_datetimes = sorted(set(frame_datetimes))
    t0 = frame_datetimes[0]

    model_times = {}
    for t in frame_datetimes:
        hours = (t - t0).total_seconds() / 3600.0
        model_times[round(hours, 6)] = t.strftime("%Y-%m-%d_%H:%M:%S")

    return model_times


def generate_default_file_tag(wrfout_dir: str, time_step: int):
    """
    Generates a default file tag based on the wrfout directory and time step.
    """
    # get last two directory names from the wrfout_dir path and join them with an underscore
    file_tag = "_".join(wrfout_dir.split("/")[-2:])
    file_tag = f"{file_tag}_dt={time_step}"
    return file_tag


def setup_dir_structure(output_dir: str):
    """
    Sets up the directory structure used by the rip container.
    It generates dedicated directories for the WRF data, RIPDP and BTrajectories outputs.

    Inputs:
    - output_dir (str): The base output directory where the subdirectories will be created.
    """
    print(f"Setting up directory structure in {output_dir}...")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "WRFData"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "RIPDP"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "BTrajectories"), exist_ok=True)


def check_dir_exists(path: str):
    """
    Used to checks if the directory structure used by the rip container is set up correctly.

    Inputs:
    - path (str): The path that should exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"The directory {path} does not exist."
            f"Please make sure the path you specified is correct and the directory structure is set up first."
        )


def check_image_exists(image_path: str):
    """
    Checks if the apptainer image exists.

    Inputs:
    - image_path (str): The path to the apptainer image.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"The apptainer image {image_path} does not exist."
            f"Please provide a valid path to the apptainer image."
        )
    if not image_path.endswith(".sif"):
        raise ValueError(
            f"The apptainer image {image_path} is not a valid .sif file."
            f"Please provide a valid path to the apptainer image, including the .sif extension."
        )


def generate_run_script(output_dir: str, script_name: str, commands: list[str]):
    """
    Generate a generic container run script with common environment setup, and append the provided commands.
    Script is saved in the output_dir and made executable.

    Inputs:
    - output_dir (str): Base output directory.
    - script_name (str): Script filename to create in output_dir.
    - commands (list[str]): Command lines to append after environment setup.

    Outputs:
    - str: Script filename.
    """
    script_path = os.path.join(output_dir, script_name)
    with open(script_path, "w") as f:
        f.write("#!/bin/bash\n")
        f.write(
            "source /miniconda3/etc/profile.d/conda.sh && conda activate ncl_stable\n"
        )
        for cmd in commands:
            f.write(f"{cmd}\n")

    os.chmod(script_path, 0o755)
    return script_name


def generate_rdp_input(
    output_dir: str,
    file_tag: str,
    time_from: int,
    time_to: int,
    time_step: int,
):
    """
    Generates the input file for the RIPDP module.

    Inputs:
    - output_dir (str): The base output directory where the RIPDP directory is located.
    - file_tag (str): The tag to identify the inputs file.
    - time_from (int): The starting time for the trajectory computation.
    - time_to (int): The ending time for the trajectory computation.
    - time_step (int): The time step for the trajectory computation.

    Outputs:
    - The path to the generated input file relative to the output_dir.
    """
    print(f"Generating RIPDP input file in {output_dir}...")
    check_dir_exists(os.path.join(output_dir, "RIPDP"))

    rdp_in = os.path.join("RIPDP", f"rdp_{file_tag}")
    with open(os.path.join(output_dir, rdp_in), "w") as f:
        f.write("&userin\n")
        f.write(f"ptimes={time_from},-{time_to},{time_step},ptimeunits='h',tacc=90.,\n")
        f.write("iexpandedout=1\n")
        f.write("/\n")

    return rdp_in


def diagnostic_groups(group_name: str):
    """
    Returns a dictionary of diagnostic fields for a given group name.

    Inputs:
    - group_name (str): The name of the diagnostic group. Valid options are:
        - "base": Basic diagnostics (latitude, longitude, elevation, pressure, geopotential height)
        - "short": temperature, potential temperature, dewpoint, humidity, wind speed/direction
        - "long": saturated equivalent potential temperature, static stability, buoyancy, CAPE/CIN

    Outputs:
    - dict[str, str]: A dictionary mapping diagnostic field names to their descriptions.
    """
    group_name = group_name.lower()
    base = {
        "xlat": "Latitude [deg]",
        "xlon": "Longitude [deg]",
        "ter": "Elevation [m]",
        "prs": "Pressure [mb]",
        "ght": "Geopotential Height [m]",
        "ghtagl": "Geopotential Height Above Ground Level [m]",
    }
    short = {
        "tmc": "Air Temperature [C]",
        "the": "Potential Temperature [K]",
        "eth": "Equivalent Potential Temperature [K]",
        "tdp": "Dewpoint Temperature [C]",
        "rhu": "Relative Humidity [%]",
        "qvp": "Water Vapor Mixing Ratio [g/kg]",
        "lcl": "Lifted Condensation Level [m]",
        "lfc": "Level of Free Convection [m]",
        "omg": "Omega [mb/s]",
        "pvm": "Moist Potential Vorticity",
        "pvo": "Potential Vorticity",
        "wsp": "Wind Speed [m/s]",
        "wdr": "Horizontal Wind Direction [deg]",
        "www": "Vertical velocity [cm/s]",
    }
    long = {
        "sateth": "Saturated Equivalent Potential Temperature [K]",
        "stb": "Static Stability [K/hPa]",
        "stbe": "Equivalent Static Stability [K/hPa]",
        "stbz": "Buoyancy [K/km]",
        "tdd": "Temperature Deficit [C]",
        "cin3": "Convective Inhibition [J/kg]",
        "cap3": "Convective Available Potential Energy [J/kg]",
        "mcap": "Most Unstable Convective Available Potential Energy [J/kg]",
        "mcin": "Most Unstable Convective Inhibition [J/kg]",
    }

    if group_name == "base":
        return base
    if group_name == "short":
        return {**base, **short}
    if group_name == "long":
        return {**base, **short, **long}
    raise ValueError("group_name must be one of: base, short, long")


def generate_point_traj_input(
    output_dir: str,
    traj_name: str,
    traj_t_0: float,
    traj_t_f: float,
    traj_dt: int,
    file_dt: int,
    traj_x: int,
    traj_y: int,
    traj_z: float,
    hydrometeor: int,
    traj_diagnostics: dict,
):
    """
    Generate a RIP input file for a single trajectory and return its path relative
    to output_dir.
    """
    print(f"Generating point trajectory input in {output_dir}/BTrajectories/...")
    check_dir_exists(os.path.join(output_dir, "BTrajectories"))

    traj_in = os.path.join("BTrajectories", f"{traj_name}.in")
    with open(os.path.join(output_dir, traj_in), "w") as f:
        f.write("&userin\n")
        f.write(" itrajcalc=1\n")
        f.write(" /\n")
        f.write(" &trajcalc\n")
        f.write(
            f" rtim={traj_t_0},ctim={traj_t_f},dtfile={file_dt}.,dttraj={traj_dt}.,vctraj='p',\n"
        )
        f.write(f" xjtraj={traj_x},\n")
        f.write(f" yitraj={traj_y},\n")
        f.write(f" zktraj={traj_z},\n")
        f.write(f" ihydrometeor={hydrometeor}\n")
        f.write(" /\n")

        # Add diagnostic fields so RIP writes .diag output when requested.
        if traj_diagnostics:
            f.write(
                "===========================================================================\n"
                "---------------------- Plot Specification Table ---------------------\n"
                "===========================================================================\n"
            )
            for diag in traj_diagnostics:
                f.write(f"feld={diag}\n")
                f.write(
                    "===========================================================================\n"
                )

    return traj_in


def generate_tabdiag_format(
    output_dir: str,
    traj_tag: str,
    traj_diagnostics: dict,
):
    """
    Generate tabdiag format file for a single trajectory and return its
    path relative to output_dir.
    """
    print(f"Generating tabdiag format in {output_dir}/BTrajectories/...")
    if traj_diagnostics == {}:
        return None

    check_dir_exists(os.path.join(output_dir, "BTrajectories"))

    tabdiag_format = os.path.join("BTrajectories", f"{traj_tag}_tabdiag_format.in")

    header = "Time [h]," + ",".join(traj_diagnostics.values())
    with open(os.path.join(output_dir, tabdiag_format), "w") as f:
        f.write(f"'{header}'\n")
        f.write(f"'({len(traj_diagnostics)+1}(3x,f9.3,3x))'\n")
    return tabdiag_format


def tabdiag_to_csv(
    traj_file: str,
    tabdiag_file: str,
    traj_diagnostics: dict,
):
    """
    Generates a CSV file from the trajectory output file.
    This is useful for post-processing and analysis of the trajectory data.

    Inputs:
    - traj_file (str): Path to the trajectory file generated by `point_trajectory`.
    - traj_diagnostics (dict): Diagnostics to be included in the CSV, as returned by `diagnostic_groups`.

    Outputs:
    - Path to generated CSV file.
    """
    print(f"Saving trajectory diagnostics to CSV...")

    if not os.path.isfile(f"{traj_file}.traj"):
        raise FileNotFoundError(f"Trajectory file not found: {traj_file}.traj")
    if not os.path.isfile(f"{traj_file}.diag"):
        raise FileNotFoundError(f"Trajectory file not found: {traj_file}.diag")
    if not os.path.isfile(f"{tabdiag_file}"):
        raise FileNotFoundError(f"Tabdiag file not found: {tabdiag_file}")

    rows = []
    with open(tabdiag_file, "r") as tf:
        for line in tf:
            s = line.strip()
            if not s or "===" in s or "Trajectory" in s or "Time [h]" in s:
                continue
            rows.append(s.split())

    if not rows:
        raise ValueError(f"No data rows found in tabdiag file: {tabdiag_file}")

    header = "Time [h]," + ",".join(traj_diagnostics.values())
    csv_file = f"{traj_file}.csv"
    with open(csv_file, "w") as cf:
        cf.write(header + "\n")
        for row in rows:
            cf.write(",".join(row) + "\n")

    return csv_file


def parse_point_traj_input(traj_in_file: str):
    """
    Parse a single-point RIP trajectory input file and extract core metadata.

    Outputs:
    - dict with keys: traj_t_0, traj_t_f, traj_z
    """
    if not os.path.isfile(traj_in_file):
        raise FileNotFoundError(f"Trajectory input file not found: {traj_in_file}")

    content = Path(traj_in_file).read_text()

    rtim_match = re.search(r"\brtim\s*=\s*([-+]?\d*\.?\d+)", content)
    ctim_match = re.search(r"\bctim\s*=\s*([-+]?\d*\.?\d+)", content)
    z_match = re.search(r"\bzktraj\s*=\s*([-+]?\d*\.?\d+)", content)

    if not rtim_match or not ctim_match or not z_match:
        raise ValueError(
            "Could not parse rtim/ctim/zktraj from trajectory input file: "
            f"{traj_in_file}"
        )

    return {
        "traj_t_0": float(rtim_match.group(1)),
        "traj_t_f": float(ctim_match.group(1)),
        "traj_z": float(z_match.group(1)),
    }


def generate_traj_plot_input(
    output_dir: str,
    plot_tag: str,
    trajectories: list[dict],
    format: str,
):
    """
    Generate a RIP plot specification input file for multiple trajectories.

    Inputs:
    - output_dir (str): Base output directory.
    - plot_tag (str): Plot input/output prefix.
    - trajectories (list[dict]): Each dict must include:
        - traj_file_rel (str): Trajectory path relative to output_dir.
        - traj_t_0 (float): Trajectory start time in model hours.
        - traj_t_f (float): Trajectory end time in model hours.
        - traj_z (float): Trajectory pressure level in hPa.
        - traj_color (str): RIP color name.

    Outputs:
    - str: Plot input file path relative to output_dir.
    """
    check_dir_exists(output_dir)

    if not trajectories:
        raise ValueError("No trajectories were provided for plotting.")

    plot_in = f"{plot_tag}.in"
    plot_path = Path(output_dir).resolve() / plot_in

    with open(plot_path, "w") as f:
        f.write(
            "&userin\n"
            " idotitle=1,titlecolor='def.foreground',\n"
            " ptimes=0,\n"
            " ptimeunits='h',tacc=120,timezone=0,iusdaylightrule=0,\n"
            " iinittime=1,ifcsttime=1,inearesth=0,\n"
            " flmin=.09, frmax=.92, fbmin=.10, ftmax=.85,\n"
            " ntextq=0,ntextcd=0,fcoffset=0.0,idotser=0,\n"
            " idescriptive=1,icgmsplit=0,maxfld=10,itrajcalc=0,imakev5d=0,\n"
            f" ncarg_type='{format}',\n"
            " /\n"
            "===========================================================================\n"
            "----------------------    Plot Specification Table    ---------------------\n"
            "===========================================================================\n"
        )

        for item in trajectories:
            traj_rel = item["traj_file_rel"]
            traj_t_0 = float(item["traj_t_0"])
            traj_t_f = float(item["traj_t_f"])
            traj_z = float(item["traj_z"])
            traj_color = item["traj_color"]

            tjst = min(traj_t_0, traj_t_f)
            tjen = max(traj_t_0, traj_t_f)

            z_label = int(round(traj_z)) if float(traj_z).is_integer() else traj_z
            t0_label = (
                int(round(traj_t_0)) if float(traj_t_0).is_integer() else traj_t_0
            )
            tf_label = (
                int(round(traj_t_f)) if float(traj_t_f).is_integer() else traj_t_f
            )
            trajectory_title = f"{z_label}_hPa_from_hour_{t0_label}_to_{tf_label}"

            f.write(f"feld=arrow; ptyp=ht; tjfl={traj_rel}; vcor=p;>\n")
            f.write(
                f"    colr={traj_color}; tjar=0.002,0.012; vwin=1000,500; tjst={tjst}; tjen={tjen};>\n"
            )
            f.write(f"    nolb; titl={trajectory_title}\n")

        f.write("feld=map; ptyp=hb\n")
        f.write("feld=tic; ptyp=hb; axlg=50\n")
        f.write(
            "===========================================================================\n"
        )

    return plot_in
