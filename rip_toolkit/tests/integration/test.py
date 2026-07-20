import rip_toolkit as ript

image_path = "RIP_legacy/ripdocker_latest.sif"

######################################################################################
######################################################################################

wrfout_dir = "RIP_legacy/Sample/WRFData"
output_dir = "tests/integration/results/Sample"
file_tag = "Sample"

mt = ript.get_model_times(wrfout_dir)
ript.print_model_times(mt)
dmt = ript.utils.date_model_times(mt)

ripdp = ript.preprocess(
    wrfout_dir=wrfout_dir,
    output_dir=output_dir,
    file_tag=file_tag,
    image_path=image_path,
)

pt_y = ript.point_trajectory(
    wrfout_dir=wrfout_dir,
    output_dir=output_dir,
    ripdp_data=ripdp,
    traj_tag="yucatan_900",
    traj_x=48,
    traj_y=17,
    traj_z=900,
    traj_t_0=dmt["2005-08-28_00:00:00"],
    traj_t_f=dmt["2005-08-28_12:00:00"],
    traj_dt=1200,
    hydrometeor=0,
    traj_diagnostics=ript.diagnostic_groups("base"),
    image_path=image_path,
)

pt_f = ript.point_trajectory(
    wrfout_dir=wrfout_dir,
    output_dir=output_dir,
    ripdp_data=ripdp,
    traj_tag="florida_900",
    traj_x=80,
    traj_y=40,
    traj_z=900,
    traj_t_0=12,
    traj_t_f=0,
    traj_dt=1200,
    hydrometeor=0,
    traj_diagnostics=ript.diagnostic_groups("base"),
    image_path=image_path,
)

st = ript.swarm_trajectories(
    wrfout_dir=wrfout_dir,
    output_dir=output_dir,
    ripdp_data=ripdp,
    traj_tag="gulf_of_mexico",
    traj_x=[50, 65],
    traj_y=[30, 45],
    traj_z=[900, 600],
    traj_t_0=0,
    traj_t_f=6,
    traj_dt=1200,
    hydrometeor=0,
    traj_diagnostics=ript.diagnostic_groups("base"),
    image_path=image_path,
)

pl = ript.plot_trajectories(
    output_dir=output_dir,
    ripdp_data=ripdp,
    traj_colors={"yucatan_900": "light.blue", "florida_900": "blue", **st},
    plot_tag="Sample_plot",
    image_path=image_path,
    format="pdf",
)

######################################################################################
######################################################################################


# wrfout_dir = "/home/francisco/Documents/SpanishPlumeAnalysis/tests/wrfdata/arwen_1"
# output_dir = "tests/integration/results/Arwen"
# file_tag = "Arwen"

# print("Model times available in wrfout_dir:")
# print(f"{ript.get_model_times(wrfout_dir)}".replace(",", "\n"))
# print()

# ripdp = ript.preprocess(
#     wrfout_dir=wrfout_dir,
#     output_dir=output_dir,
#     file_tag=file_tag,
#     image_path=image_path,
# )

# ripdp = "tests/integration/results/Arwen/RIPDP/rdp_Arwen"

# st = ript.stack_trajectories(
#     wrfout_dir=wrfout_dir,
#     output_dir=output_dir,
#     ripdp_data=ripdp,
#     traj_tag="NorthSea",
#     traj_x=230,
#     traj_y=200,
#     traj_z=[900, 800, 700, 600, 500],
#     traj_t_0=43,
#     traj_t_f=45.66667,
#     traj_dt=300,
#     hydrometeor=0,
#     traj_diagnostics=ript.diagnostic_groups("base"),
#     image_path=image_path,
# )
# pl = ript.plot_trajectories(
#     output_dir=output_dir,
#     ripdp_data=ripdp,
#     traj_colors={**st},
#     plot_tag="Arwen_plot",
#     image_path=image_path,
#     format="pdf",
# )
