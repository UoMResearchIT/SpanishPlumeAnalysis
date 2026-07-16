import os
from pathlib import Path
import subprocess
from rip_toolkit.utils import (
    get_model_times,
    generate_default_file_tag,
    setup_dir_structure,
    check_dir_structure,
    check_image_exists,
    generate_rdp_input,
    generate_rdp_run_script,
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
    It bind mounts the output directory and the wrfout directory.
    Then it runs the run_script inside the container specified by the image.
    """
    print(f"Running RIP container with image {image_path}...")
    rel_outdir = output_dir
    check_dir_structure(output_dir)
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

    print(f"Container finished successfully. Outputs saved to: {rel_outdir}/RIPDP/")
    with open(os.path.join(ripdp_dir, f"rdp_{file_tag}.xtimes"), "r") as f:
        xt = f.read().splitlines()
        print(f"Preprocessed a total of {xt[0].replace(' ', '')} times:")
        for line in xt[1:]:
            print(f"  {line}")


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
    - output_dir (str): Directory where the RIPDP data will be saved.
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

    return os.path.join(output_dir, "RIPDP")


def point_trajectory():
    """
    Computes the trajectory of a single point.
    """
    pass


def swarm_trajectory():
    """
    Computes the trajectory of a swarm of points.
    """
    pass
