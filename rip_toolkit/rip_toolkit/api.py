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
    generate_point_traj_input,
    diagnostic_groups,
    generate_point_tabdiag_format,
    generate_point_tabdiag_to_csv_script,
    generate_point_traj_run_script,
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
        print(f"Starting container...")
        cp = subprocess.run(
            apptainer_command,
            check=True,
            text=True,
            capture_output=True,  # captures both stdout/stderr
        )
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
    if file_tag is None:
        file_tag = generate_default_file_tag(wrfout_dir, time_step)

    mt = get_model_times(wrfout_dir)
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
    print(f"Preprocessing done. Outputs saved to: {output_dir}/RIPDP/")
    with open(xtimes_file, "r") as f:
        xt = f.read().splitlines()
        print(f"Preprocessed a total of {xt[0].replace(' ', '')} times:")
        for line in xt[1:]:
            print(f"  {line}")

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
    - image_path (str): Path to apptainer image.

    Outputs:
    - Path to generated trajectory file.
    """
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
    )
    run_script = generate_point_traj_run_script(
        output_dir=output_dir,
        rdp_in=rdp_in,
        traj_in=traj_in,
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
    print(f"Trajectory computation done. Outputs saved to: {traj_file}*")

    return f"{traj_file}.traj"


def swarm_trajectory():
    """
    Computes the trajectory of a swarm of points.
    """
    pass
