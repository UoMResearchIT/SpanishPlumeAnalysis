# python script to create input files for skewT animations along trajectories
# The script generates two files, one for the generation of the trajectories and another for the skewT plots:
#   - rip_skewT_trajectories.inputs
#   - skewT_trajectories.inputs
# From the base directory, the following commands will generate the skewT animations.
#   $ conda activate wrf-py-env
#   $ python3 CSF/generate_skewT_traj_inputs.py
#   $ RIP/CSF/Submit.sh rip_skewT_trajectories.inputs Results/SkewT_Trajectories/
#   $ ./CSF/Submit.sh Results/skewT_trajectories.inputs Results/SkewT_Trajectories/
# However, make sure that you wait for the trajectory generation to finish before running the skewT generation.

import sys, os

sys.path.insert(1, "/".join(__file__.split("/")[:-2]))

# Base data directory path
base_dir_path = "/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/"
# List of simulations
simulations = [
    # {"wrfout":"control",                            "output":"rip"},      # For local tests called from src directory
    {"output": "Control", "wrfout": "run-zrek"},
    # {"output": "G_Wave_fix", "wrfout": "run-zrek.gravity_wave.CON_OA_fix"},
    # {"output": "Double_hgt", "wrfout": "run-zrek.double_hgt"},
    # {"output": "Half_hgt", "wrfout": "run-zrek.half_hgt"},
    # {"output": "Zero_hgt", "wrfout": "run-zrek.zero_hgt"},
    # {"output": "Albedo_90", "wrfout": "run-zrek.albedo_90"},
    # {"output": "Albedo_Standard", "wrfout": "run-zrek.albedo_standard"},
    # {"output": "Albedo_40", "wrfout": "run-zrek.albedo_40"},
    # {"output": "Morrison", "wrfout": "run-zrek.morrison_microphysics"},
    # {"output": "Thompson", "wrfout": "run-zrek.thompson_microphysics"},
    # {"output": "Dom2", "wrfout": "run-zrek.2domains"},
]


##########################################################

# Generate trajectory CSV files
# List of trajectory starting points
trajectory_locations = [
    # {"name":"Aberporth",    "x":"179", "y":"407"},
    # {"name": "Algeria", "x": "172", "y": "251"},
    # {"name":"Camborne",     "x":"173", "y":"392"},
    # {"name": "Gibraltar", "x": "158", "y": "287"},
    # {"name":"Herstmonceux"  "x":"202", "y":"395"},
    # {"name": "LaCoruna", "x": "149", "y": "343"},
    # {"name": "Larkhill", "x": "191", "y": "398"},
    # {"name":"Lerwick",      "x":"202", "y":"470"},
    # {"name": "Madrid", "x": "172", "y": "317"},
    # {"name": "Murcia", "x": "184", "y": "297"},
    # {"name": "Nimes", "x": "219", "y": "339"},
    {"name": "Nottingham", "x": "195", "y": "412"},
    # {"name": "Santander", "x": "174", "y": "340"},
    # {"name":"Stornoway",    "x":"178", "y":"457"},
    # {"name": "Trappes", "x": "209", "y": "377"},
]
trajectory_times = [
    # Forward
    # "38-68",
    # "92-122",
    # "0-80",
    # "45-125",
    # Backward
    # "54-0",
    # "57-0",
    "60-0",
    "66-0",
    # "114-54",
    # "114-0",
    # "120-54",
    # "120-0",
    # "68-38",
    # "122-92",
    # "80-0",
    # "125-45",
]
# Build trajectory list
trajectory_list = []
for location in trajectory_locations:
    for times in trajectory_times:
        trajectory_list.append(
            {
                "times": times,
                "x": location["x"],
                "y": location["y"],
                "name": location["name"],
            }
        )

wrfout_dir = "/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/"
base_dir = "/mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/"
rip_dir = f"{base_dir}Analysis/RIP/"
results_dir = f"{base_dir}SpanishPlumeAnalysis/Results/"
ripdp_dir = f"{rip_dir}Results/RIPDP/"
traj_dir = f"{results_dir}Trajectories/"
traj_csv_paths = []

# Create inputs for Trajectory generation
name = "rip_skewT_trajectories.inputs"
with open(name, "w") as file:
    # Iterate through trajectories and simulations (trajectories first to prevent errors when creating folders)
    for trajectory in trajectory_list:
        for sim in simulations:
            file.write(
                f"-tt={trajectory['times']} --traj_x={trajectory['x']} --traj_y={trajectory['y']} "
            )
            tp = f"{sim['output']}_{trajectory['name']}_{trajectory['times']}"
            pd = f"{ripdp_dir}{sim['output']}/rdp_{sim['output']}"
            od = f"{traj_dir}{sim['output']}"
            file.write(f"-tp={tp} -pd={pd} -od={od}\n")
            traj_csv_paths.append(f"{od}/{tp}")
        file.write("\n")

##########################################################

##########################################################

# Generate inputs for skewT trajectory generation
# Get pressure levels from traj_inputs.template
pressure_levels = []
with open("RIP/Templates/traj_inputs.template", "r") as file:
    next(file)  # Skip the header line
    for line in file:
        columns = line.split()
        pressure_level = int(
            columns[6]
        )  # Pressure level is in the 7th column (0-indexed)
        pressure_levels.append(pressure_level)
# Generate trajectory csv path list
traj_csv_paths_with_p = []
for path in traj_csv_paths:
    p_levs = []
    for pressure_level in pressure_levels:
        p_levs.append(f"{path}_{pressure_level}hPa")
    traj_csv_paths_with_p.append(p_levs)

# Options
options = [
    "--save_pdf_frames=1",
]
opts = " ".join(options)

# Padding for task and wrf data paths
pad_task = 19
pad_var = 24
pad_traj = max(len(tcpwp) for tcpwp in traj_csv_paths_with_p) + 2
pad_wrf = (
    max(len(simulation["wrfout"]) for simulation in simulations)
    + len(base_dir_path)
    + 13
)
pad_opts = len(opts) + 15

# Generate skewt inputs
with open("skewT_trajectories.inputs", "w") as file:
    for simulation in simulations:
        for tcp in traj_csv_paths_with_p:
            for tcpwp in tcp:
                task = "--task=diagnostic"
                var = f"--var=SkewT_Trajectory"
                traj = f"--traj={tcpwp}.csv"
                dir_path = f"--dir_path={base_dir_path}{simulation['wrfout']}/"
                opts_dom = opts
                if simulation["output"] in ["Albedo_90", "Dom2"]:
                    opts_dom = opts + " --domain=full"
                od = os.path.dirname(tcpwp)
                outdir = f"--outdir={od}/SkewTs/"

                file.write(
                    f"{task:<{pad_task}} {var:<{pad_var}} {traj:<{pad_traj}} {dir_path:<{pad_wrf}} {opts_dom:<{pad_opts}} {outdir}\n"
                )
            file.write("\n")
        file.write("\n")
