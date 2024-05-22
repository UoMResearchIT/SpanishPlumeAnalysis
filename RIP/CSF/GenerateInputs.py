# python script to create input files for RIPDP

# List of simulations
simulations = [
    # {"wrfout":"control",                            "output":"rip"},      # For local tests called from src directory
    {"wrfout": "run-zrek", "output": "Control"},
    # {"wrfout": "run-zrek.gravity_wave.CON_OA_fix", "output": "G_Wave_fix"},
    # {"wrfout": "run-zrek.double_hgt", "output": "Double_hgt"},
    # {"wrfout": "run-zrek.half_hgt", "output": "Half_hgt"},
    # {"wrfout": "run-zrek.zero_hgt", "output": "Zero_hgt"},
    {"wrfout": "run-zrek.albedo_90", "output": "Albedo_90"},
    {"wrfout": "run-zrek.albedo_standard", "output": "Albedo_Standard"},
    {"wrfout": "run-zrek.albedo_40", "output": "Albedo_40"},
    # {"wrfout": "run-zrek.morrison_microphysics", "output": "Morrison"},
    # {"wrfout": "run-zrek.thompson_microphysics", "output": "Thompson"},
]
# List of trajectories
# Aberporth,Algeria,Camborne,Gibraltar,Herstmonceux,LaCoruna,Larkhill,Lerwick,Madrid,Murcia,Nimes,Nottingham,Santander,Stornoway,Trappes
trajectory_locations = [
    # {"name":"Aberporth",    "x":"179", "y":"407"},
    # {"name": "Algeria", "x": "172", "y": "251"},
    # {"name":"Camborne",     "x":"173", "y":"392"},
    # {"name": "Gibraltar", "x": "158", "y": "287"},
    # {"name":"Herstmonceux"  "x":"202", "y":"395"},
    # {"name": "LaCoruna", "x": "149", "y": "343"},
    # {"name":"Larkhill",     "x":"191", "y":"398"},
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
    "60-0",
    "66-0",
    "114-54",
    "114-0",
    "120-54",
    "120-0",
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
# Diagnostics
diags = [
    # "none",
    # "",
    "g1",
    "g2",
    # "all",
]

wrfout_dir = "/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/"
rip_dir = "/mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/RIP/"
results_dir = f"{rip_dir}Results/"
ripdp_dir = f"{results_dir}RIPDP/"
traj_dir = f"{rip_dir}Results/Trajectories/"
# For local tests called from src directory
# ripdp_dir="tests/results/rip/RIPDP/"
# traj_dir=f"tests/results/rip/"


# Create inputs for RIPDP pre-processing
name = "RIPDP.inputs"
with open(name, "w") as file:
    # Iterate through simulations
    for sim in simulations:
        file.write(
            f"-wd={wrfout_dir}{sim['wrfout']} -od={results_dir}{sim['output']} -nt -np\n"
        )


# Create inputs for Trajectory generation
name = "Trajectories.inputs"
with open(name, "w") as file:
    # Iterate through trajectories and simulations (trajectories first to prevent errors when creating folders)
    for trajectory in trajectory_list:
        for sim in simulations:
            for diag in diags:
                file.write(
                    f"-tt={trajectory['times']} --traj_x={trajectory['x']} --traj_y={trajectory['y']} -td={diag} "
                )
                file.write(
                    f"-tp={sim['output']}_{trajectory['name']}_{trajectory['times']} "
                )
                file.write(
                    f"-pd={ripdp_dir}{sim['output']}/rdp_{sim['output']} -od={traj_dir}{sim['output']}\n"
                )
        file.write("\n")


# Create inputs for swarm Trajectories
name = "SwarmTrajectories.inputs"
sim = simulations[0]
p_levs = [
    "925",
    "850",
    "700",
    "500",
    "300",
    "250",
]
trajectory_times = [
    # Forward
    # Backward
    "60-0",
    "66-0",
    "114-0",
    "120-0",
]
with open(name, "w") as file:
    # Iterate through simulations
    for tt in trajectory_times:
        for p_lev in p_levs:
            file.write(f"-tt={tt} -td=none --swarm --swarm_p={p_lev}")
            file.write(f"-tp={sim['output']}_swarm_{p_lev}_{tt} ")
            file.write(
                f"-pd={ripdp_dir}{sim['output']}/rdp_{sim['output']} -od={traj_dir}{sim['output']}\n"
            )
        file.write("\n")
