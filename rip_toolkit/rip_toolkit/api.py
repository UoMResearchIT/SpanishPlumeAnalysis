import os
from pathlib import Path
import subprocess
from .utils import (
    get_model_times,
    generate_default_file_tag,
    setup_dir_structure,
    check_dir_exists,
    check_image_exists,
    generate_rdp_input,
    generate_rdp_run_script,
    diagnostic_groups,
    generate_point_traj_input,
    generate_tabdiag_format,
    generate_point_traj_run_script,
    tabdiag_to_csv,
    parse_point_traj_input,
    generate_traj_plot_input,
    generate_traj_plot_run_script,
)


def run_rip_container(
    wrfout_dir: str,
    output_dir: str,
    ripdp_dir: str,
    file_tag: str,
    image_path: str,
    run_script: str,
):
    """
    Calls apptainer to run the rip_toolkit commands.
    It bind mounts the output directory, the RIPDP directory, and the wrfout directory.
    Then it runs the run_script inside the container specified by the image.
    """
    print(f"Running RIP container with image {image_path}...")
    check_dir_exists(output_dir)
    check_image_exists(image_path)
    wrfout_dir = Path(wrfout_dir).resolve()
    output_dir = Path(output_dir).resolve()
    ripdp_dir = Path(ripdp_dir).resolve()
    image_path = Path(image_path).resolve()
    run_script = run_script

    apptainer_command = [
        "apptainer",
        "exec",
        "--contain",
        "--cleanenv",
        f"--bind={output_dir}/:/{file_tag}/",
        f"--bind={wrfout_dir}/:/{file_tag}/WRFData/",
        f"--bind={ripdp_dir}/:/{file_tag}/RIPDP/",
        "--pwd",
        f"/{file_tag}",
        f"{image_path}",
        "/bin/bash",
        f"{run_script}",
    ]
    try:
        print(f"Starting rip container...")
        cp = subprocess.run(
            apptainer_command,
            check=True,
            text=True,
            capture_output=True,  # captures both stdout/stderr
        )
        if cp.stdout:
            print(cp.stdout)
        if cp.stderr:
            print(cp.stderr)
    except subprocess.CalledProcessError as e:
        msg = (
            "Container failed.\n"
            f"  --- Command --\n    {' '.join(apptainer_command)}\n"
            f"  --- stdout ---\n    {e.stdout or ''}\n"
            f"  --- stderr ---\n    {e.stderr or ''}"
        )
        raise RuntimeError(msg) from None


def preprocess(
    wrfout_dir: str,
    output_dir: str,
    file_tag: str | None = None,
    time_from: float = 0,
    time_to: float | None = None,
    time_step: float | None = None,
    image_path: str = "ripdocker_latest.sif",
):
    """
    This step only needs to be performed once per set of wrf data, and can be reused to compute many trajectories a posteriori.
    It creates the output directory and, inside it, a `RIPDP` directory, where it saves all the preprocessing outputs.

    Inputs:
    - wrfout_dir (str): Path to the directory containing the wrfout files.
    - output_dir (str): Directory where the RIPDP directory will be created and populated.
    - file_tag (str | None): A tag to identify the run of the preprocessing.
    - time_from (float): Start model time for preprocessing, in hours since simulation start (inclusive).
    - time_to (float | None): End model time for preprocessing, in hours since simulation start (inclusive).
    - time_step (float): Requested RIPDP output interval in hours for ptimes. RIPDP can only emit times that exist in the provided WRF history data.

    *Note: model times can be obtained from the wrfout files using the `get_model_times` function in `rip_toolkit.utils`.

    Outputs:
    - The path to the RIPDP directory containing the preprocessing outputs.
    """
    print(f"Starting preprocessing of {wrfout_dir} data...")
    if file_tag is None:
        file_tag = generate_default_file_tag(wrfout_dir, time_step)

    mt = get_model_times(wrfout_dir)
    if len(mt) < 2:
        raise ValueError(
            f"Not enough model times found in wrfout_dir ({wrfout_dir}) to perform preprocessing. Found: {mt}"
        )
    if time_to is None:
        time_to = max(mt.keys())
    if time_from < min(mt.keys()):
        raise ValueError(
            f"time_from ({time_from}) is less than the minimum model time ({min(mt.keys())})"
        )
    if time_to > max(mt.keys()):
        raise ValueError(
            f"time_to ({time_to}) is greater than the maximum model time ({max(mt.keys())})"
        )
    mt_time_step = sorted(mt.keys())[1] - sorted(mt.keys())[0]

    if time_step is None:
        time_step = mt_time_step
    if time_step < mt_time_step:
        raise ValueError(
            f"time_step ({time_step}) is less than the minimum time step in the model data ({mt_time_step})"
        )

    setup_dir_structure(output_dir)
    rdp_in = generate_rdp_input(
        output_dir,
        file_tag=file_tag,
        time_from=time_from,
        time_to=time_to,
        time_step=time_step,
    )
    run_script = generate_rdp_run_script(output_dir, rdp_in=rdp_in)
    run_rip_container(
        wrfout_dir=wrfout_dir,
        output_dir=output_dir,
        ripdp_dir=os.path.join(output_dir, "RIPDP"),
        file_tag=file_tag,
        image_path=image_path,
        run_script=run_script,
    )

    xtimes_file = os.path.join(output_dir, "RIPDP", f"rdp_{file_tag}.xtimes")
    if not os.path.isfile(xtimes_file):
        print(
            f"ERROR: Preprocessing container is done, but the expected xtimes file was not found: {xtimes_file}"
        )
    print(f"\nPreprocessing done.")
    with open(xtimes_file, "r") as f:
        xt = f.read().splitlines()
        print(f"Preprocessed a total of {xt[0].replace(' ', '')} times:")
        for line in xt[1:]:
            print(f"  {line}")
    print(f"Outputs saved to: {output_dir}/RIPDP/\n")

    return os.path.join(output_dir, rdp_in)


def point_trajectory(
    wrfout_dir: str,
    output_dir: str,
    ripdp_data: str,
    traj_tag: str,
    traj_x: int,
    traj_y: int,
    traj_z: float,
    traj_t_0: float,
    traj_t_f: float,
    traj_dt: int = 600,
    file_dt: int | None = None,
    hydrometeor: int = 0,
    traj_diagnostics: dict = diagnostic_groups("base"),
    image_path: str = "ripdocker_latest.sif",
):
    """
    Computes a single trajectory using existing RIPDP preprocessed data.

    Inputs:
    - wrfout_dir (str): Path to the directory containing wrfout files.
    - output_dir (str): Directory where trajectory files will be saved.
    - ripdp_data (str): Full path to the RIPDP prefix file (e.g. RIPDP/rdp_test) generated by the preprocess function.
    - traj_tag (str): A tag to identify the trajectory.
    - traj_t_0 (float): Particle release time (model time) in minutes.
    - traj_t_f (float): Time until which the trajectory will be computed (model time) in minutes.
    - traj_x (int): Grid x position from which the particle is released.
    - traj_y (int): Grid y position from which the particle is released.
    - traj_z (float): Pressure level (hPa).
    - traj_dt (int): Trajectory numerical timestep (seconds).
    - file_dt (int): Time interval in RIPDP data (seconds).
    - hydrometeor (int): Set to 0 for Air Parcel trajectories, or 1 for Hydrometeor trajectories.
    - traj_diagnostics (dict): Diagnostics to be computed along trajectory, as returned by `diagnostic_groups(group_name)`.
    - image_path (str): Path to apptainer image.

    Outputs:
    - Path to generated trajectory file.
    """
    print(f"Computing trajectory '{traj_tag}'...")

    setup_dir_structure(output_dir)

    ripdp_data = str(Path(ripdp_data).resolve())
    ripdp_dir = str(Path(ripdp_data).parent)
    rdp_in = f"RIPDP/{Path(ripdp_data).name}"

    if file_dt is None:
        xtimes_file = os.path.join(ripdp_dir, f"{Path(rdp_in).name}.xtimes")
        if not os.path.isfile(xtimes_file):
            raise ValueError(
                "file_dt was not provided and could not be inferred because "
                f"xtimes file does not exist: {xtimes_file}. "
                "Please pass file_dt explicitly in seconds."
            )

        with open(xtimes_file, "r") as f:
            lines = [ln.strip() for ln in f.readlines() if ln.strip()]

        # ripdp xtimes starts with a count line followed by model times.
        times = []
        for ln in lines[1:]:
            try:
                times.append(float(ln))
            except ValueError:
                continue

        if len(times) < 2:
            raise ValueError(
                "file_dt was not provided and xtimes does not contain enough "
                f"time entries to infer it: {xtimes_file}. "
                "Please pass file_dt explicitly in seconds."
            )

        file_dt = int(round((times[1] - times[0]) * 3600))

    if file_dt <= 0:
        raise ValueError(f"Invalid file_dt: {file_dt}. It must be > 0 seconds.")

    traj_name = f"{traj_tag}_traj_point"
    traj_in = generate_point_traj_input(
        output_dir=output_dir,
        traj_name=traj_name,
        traj_t_0=traj_t_0,
        traj_t_f=traj_t_f,
        traj_dt=traj_dt,
        file_dt=file_dt,
        traj_x=traj_x,
        traj_y=traj_y,
        traj_z=traj_z,
        hydrometeor=hydrometeor,
        traj_diagnostics=traj_diagnostics,
    )
    tabdiag_format = generate_tabdiag_format(
        output_dir=output_dir,
        traj_tag=traj_tag,
        traj_diagnostics=traj_diagnostics,
    )
    run_script = generate_point_traj_run_script(
        output_dir=output_dir,
        rdp_in=rdp_in,
        traj_in=traj_in,
        tabdiag_format=tabdiag_format,
    )

    run_rip_container(
        wrfout_dir=wrfout_dir,
        output_dir=output_dir,
        ripdp_dir=ripdp_dir,
        file_tag=traj_tag,
        image_path=image_path,
        run_script=run_script,
    )

    traj_file = os.path.join(output_dir, "BTrajectories", traj_name)

    if traj_diagnostics != {}:
        tabdiag_to_csv(
            traj_file=traj_file,
            tabdiag_file=traj_file + ".tabdiag",
            traj_diagnostics=traj_diagnostics,
        )

    print(f"\nTrajectory computation done.")
    print(f"Outputs saved to: {traj_file}*\n")

    return f"{traj_file}.traj"


def swarm_trajectory():
    """
    Computes the trajectory of a swarm of points.
    """
    pass


def plot_trajectories(
    output_dir: str,
    ripdp_data: str,
    traj_colors: dict[str, str],
    plot_tag: str,
    format: str = "pdf",
    image_path: str = "ripdocker_latest.sif",
):
    """
    Generate trajectory plot from the trajectory(ies) specified.

    Inputs:
    - output_dir (str): Output directory used by the RIP workflow (must contain `BTrajectories` directory).
    - ripdp_data (str): Full path to the RIPDP prefix file (e.g. RIPDP/rdp_test) generated by the preprocess function.
    - traj_colors (dict[str, str]): A dictionary with trajecory tags as keys and colors as values (`{traj_tag: rip_color}`).
      For each key `traj_tag`, a `BTrajectories/{traj_tag}.traj` or `BTrajectories/{traj_tag}_traj_point.traj` is expected.
    - file_tag (str | None): A tag to identify the plot.
    - image_path (str): Path to apptainer image.

    Outputs:
    - Path to generated plot file (`.pdf`).
    """
    print(f"Generating trajectory plot...")
    if not traj_colors:
        raise ValueError("traj_colors must contain at least one traj_tag -> color pair")

    setup_dir_structure(output_dir)

    output_abs = Path(output_dir).resolve()
    rdp_in_abs = Path(ripdp_data).resolve()
    ripdp_dir = rdp_in_abs.parent
    rdp_in_rel = f"RIPDP/{rdp_in_abs.name}"
    btraj_dir = output_abs / "BTrajectories"
    if not btraj_dir.is_dir():
        raise FileNotFoundError(f"BTrajectories directory not found: {btraj_dir}")

    trajectories = []
    for traj_tag, traj_color in traj_colors.items():
        direct = btraj_dir / f"{traj_tag}.traj"
        point = btraj_dir / f"{traj_tag}_traj_point.traj"
        if direct.is_file():
            traj_abs = direct
        elif point.is_file():
            traj_abs = point
        else:
            raise FileNotFoundError(
                "Could not find trajectory file for tag "
                f"'{traj_tag}'. Looked for: {direct.name}, {point.name}"
            )

        traj_in_file = str(traj_abs.with_suffix(".in"))
        parsed = parse_point_traj_input(traj_in_file)

        trajectories.append(
            {
                "traj_file_rel": str(traj_abs.relative_to(output_abs)),
                "traj_t_0": parsed["traj_t_0"],
                "traj_t_f": parsed["traj_t_f"],
                "traj_z": parsed["traj_z"],
                "traj_color": traj_color,
            }
        )

    plot_in = generate_traj_plot_input(
        output_dir=output_dir,
        plot_tag=plot_tag,
        trajectories=trajectories,
        format=format,
    )
    run_script = generate_traj_plot_run_script(
        output_dir=output_dir,
        rdp_in=rdp_in_rel,
        plot_in=plot_in,
    )

    run_rip_container(
        wrfout_dir=os.path.join(output_dir, "WRFData"),
        output_dir=output_dir,
        ripdp_dir=str(ripdp_dir),
        file_tag=plot_tag,
        image_path=image_path,
        run_script=run_script,
    )

    plot_file = os.path.join(output_dir, f"{plot_tag}.pdf")
    if not os.path.isfile(plot_file):
        print(
            f"WARNING: Plot container run completed but expected pdf file was not found: {plot_file}"
        )
    else:
        print(f"\nTrajectory plot done.")
        print(f"Output saved to: {plot_file}\n")

    return plot_file
