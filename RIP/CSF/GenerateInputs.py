# python script to create input files for RIPDP

# List of simulations
simulations = [
    # {"wrfout":"control",                            "output":"rip"},      # For local tests called from src directory
    {"wrfout":"run-zrek",                           "output":"Control"},
    {"wrfout":"run-zrek.gravity_wave.CON_OA_fix",   "output":"G_Wave_fix"},
    {"wrfout":"run-zrek.double_hgt",                "output":"Double_hgt"},
    {"wrfout":"run-zrek.half_hgt",                  "output":"Half_hgt"},
    {"wrfout":"run-zrek.zero_hgt",                  "output":"Zero_hgt"},
    {"wrfout":"run-zrek.albedo_90",                 "output":"Albedo_90"},
    {"wrfout":"run-zrek.albedo_standard",           "output":"Albedo_Standard"},
    {"wrfout":"run-zrek.albedo_40",                 "output":"Albedo_40"},
    {"wrfout":"run-zrek.morrison_microphysics",     "output":"Morrison"},
    {"wrfout":"run-zrek.thompson_microphysics",     "output":"Thompson"},
]
# List of trajectories
#Aberporth,Algeria,Camborne,Gibraltar,Herstmonceux,LaCoruna,Larkhill,Lerwick,Madrid,Murcia,Nimes,Nottingham,Santander,Stornoway,Trappes
trajectory_locations = [
    # {"name":"Aberporth",    "x":"407", "y":"179"},
    {"name":"Algeria",      "x":"251", "y":"172"},
    # {"name":"Camborne",     "x":"392", "y":"173"},
    {"name":"Gibraltar",    "x":"287", "y":"158"},
    # {"name":"Herstmonceux"  "x":"395", "y":"202"},
    {"name":"LaCoruna",     "x":"343", "y":"149"},
    # {"name":"Larkhill",     "x":"398", "y":"191"},
    # {"name":"Lerwick",      "x":"470", "y":"202"},
    {"name":"Madrid",       "x":"317", "y":"172"},
    {"name":"Murcia",       "x":"297", "y":"184"},
    {"name":"Nimes",        "x":"339", "y":"219"},
    {"name":"Nottingham",   "x":"412", "y":"195"},
    {"name":"Santander",    "x":"340", "y":"174"},
    # {"name":"Stornoway",    "x":"457", "y":"178"},
    {"name":"Trappes",      "x":"377", "y":"209"},

]
trajectory_times = [
    #Forward
    "75-125",
    "20-70",
    #Backward
    "125-75",
    "70-20",
]
#Build trajectory list
trajectory_list=[]
for location in trajectory_locations:
    for times in trajectory_times:
        trajectory_list.append({"times":times, "x":location["x"], "y":location["y"], "name":location["name"]})

wrfout_dir="/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/"
rip_dir="/mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/RIP/"
results_dir=f"{rip_dir}Results/"
ripdp_dir=f"{results_dir}RIPDP/"
traj_dir=f"{rip_dir}Results/Trajectories/"
# For local tests called from src directory
# ripdp_dir="tests/results/rip/RIPDP/"
# traj_dir=f"tests/results/rip/"


# Create inputs for RIPDP pre-processing
name="RIPDP.inputs"
with open(name, 'w') as file:
    #Iterate through simulations
    for sim in simulations:
        file.write(f"-wd={wrfout_dir}{sim['wrfout']} -od={results_dir}{sim['output']} -nt -np\n")


# Create inputs for Trajectory generation
name="Trajectories.inputs"
with open(name, 'w') as file:
    # Iterate through trajectories and simulations (trajectories first to prevent errors when creating folders)
    for trajectory in trajectory_list:
        for sim in simulations:
            file.write(f"-tt={trajectory['times']} --traj_x={trajectory['x']} --traj_y={trajectory['y']} ")
            file.write(f"-tp={sim['output']}_{trajectory['name']}_{trajectory['times']} ")
            file.write(f"-pd={ripdp_dir}{sim['output']}/rdp_{sim['output']} -od={traj_dir}{sim['output']}\n")
        file.write("\n")

