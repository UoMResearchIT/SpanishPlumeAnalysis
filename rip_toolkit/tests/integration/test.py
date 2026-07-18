import rip_toolkit as ript

wrfout_dir = "RIP_legacy/Sample/WRFData"
output_dir = "tests/integration/results"
file_tag = "test"
image_path = "RIP_legacy/ripdocker_latest.sif"

print("Model times available in wrfout_dir:")
print(f"{ript.get_model_times(wrfout_dir)}".replace(",", "\n"))
print()

ripdp = ript.preprocess(
    wrfout_dir=wrfout_dir,
    output_dir=output_dir,
    file_tag=file_tag,
    image_path=image_path,
)


tp = ript.point_trajectory(
    wrfout_dir=wrfout_dir,
    output_dir=output_dir,
    ripdp_data=ripdp,
    traj_tag="yucatan_900",
    traj_x=48,
    traj_y=17,
    traj_z=900,
    traj_t_0=0,
    traj_t_f=12,
    traj_dt=1200,
    hydrometeor=0,
    traj_diagnostics=ript.diagnostic_groups("base"),
    image_path=image_path,
)

tp = ript.point_trajectory(
    wrfout_dir=wrfout_dir,
    output_dir=output_dir,
    ripdp_data=ripdp,
    traj_tag="florida_900",
    traj_x=80,
    traj_y=40,
    traj_z=900,
    traj_t_0=0,
    traj_t_f=12,
    traj_dt=1200,
    hydrometeor=0,
    traj_diagnostics=ript.diagnostic_groups("base"),
    image_path=image_path,
)

pl = ript.plot_trajectories(
    output_dir=output_dir,
    ripdp_data=ripdp,
    traj_colors={"yucatan_900": "green", "florida_900": "red"},
    plot_tag="test_plot",
    image_path=image_path,
)
