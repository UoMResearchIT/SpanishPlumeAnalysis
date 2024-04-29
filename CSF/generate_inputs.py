# python script to create input files for all simulations

import sys

sys.path.insert(1, "/".join(__file__.split("/")[:-2]))

# Base data directory path
base_dir_path = "/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/"
# List of simulations
simulations = [
    # {"wrfout":"control",                            "output":"rip"},      # For local tests called from src directory
    {"output": "Control", "wrfout": "run-zrek"},
    {"output": "G_Wave_fix", "wrfout": "run-zrek.gravity_wave.CON_OA_fix"},
    {"output": "Double_hgt", "wrfout": "run-zrek.double_hgt"},
    {"output": "Half_hgt", "wrfout": "run-zrek.half_hgt"},
    {"output": "Zero_hgt", "wrfout": "run-zrek.zero_hgt"},
    {"output": "Albedo_90", "wrfout": "run-zrek.albedo_90"},
    {"output": "Albedo_Standard", "wrfout": "run-zrek.albedo_standard"},
    {"output": "Albedo_40", "wrfout": "run-zrek.albedo_40"},
    {"output": "Morrison", "wrfout": "run-zrek.morrison_microphysics"},
    {"output": "Thompson", "wrfout": "run-zrek.thompson_microphysics"},
    {"output": "Dom2", "wrfout": "run-zrek.2domains"},
]

# Options
options = [
    "--save_pdf_frames=1",
]
opts = " ".join(options)

# Diagnostics

import SensibleVariables as sv

sens_vars = [
    attr
    for attr in dir(sv)
    if not callable(getattr(sv, attr)) and not attr.startswith("__")
]

# all sens_vars that dont start with skewt
diagnostics = [var for var in sens_vars if not var.startswith("SkewT")]
# skewt variables
skewts = [var for var in sens_vars if var.startswith("SkewT")]
skewts.remove("SkewT")  # remove generic SkewT

# Padding for task and wrf data paths
pad_task = 19
pad_wrf = (
    max(len(simulation["wrfout"]) for simulation in simulations)
    + len(base_dir_path)
    + 13
)
pad_opts = len(opts) + 15

# Generate diagnostic inputs
pad_var = max(len(diagnostic) for diagnostic in diagnostics) + 7
with open("all_diag.inputs", "w") as file:
    for simulation in simulations:
        for diagnostic in diagnostics:
            task = "--task=diagnostic"
            var = f"--var={diagnostic}"
            dir_path = f"--dir_path={base_dir_path}{simulation['wrfout']}/"
            opts_dom = opts
            if simulation["output"] in ["Albedo_90", "Dom2"]:
                opts_dom = opts + " --domain=full"
            outdir = f"--outdir={simulation['output']}/"

            file.write(
                f"{task:<{pad_task}} {var:<{pad_var}} {dir_path:<{pad_wrf}} {opts_dom:<{pad_opts}} {outdir}\n"
            )
        file.write("\n")

# Generate skewt inputs
pad_var = max(len(skewt) for skewt in skewts) + 7
with open("all_skewt.inputs", "w") as file:
    for simulation in simulations:
        for skewt in skewts:
            task = "--task=diagnostic"
            var = f"--var={skewt}"
            dir_path = f"--dir_path={base_dir_path}{simulation['wrfout']}/"
            opts_dom = opts
            if simulation["output"] in ["Albedo_90", "Dom2"]:
                opts_dom = opts + " --domain=full"
            outdir = f"--outdir={simulation['output']}/"

            file.write(
                f"{task:<{pad_task}} {var:<{pad_var}} {dir_path:<{pad_wrf}} {opts_dom:<{pad_opts}} {outdir}\n"
            )
        file.write("\n")
