import rip_toolkit as ript

wrfout_dir = "RIP_legacy/Sample/WRFData"
output_dir = "tests/integration/results"
file_tag = "test"
image_path = "RIP_legacy/ripdocker_latest.sif"

print("Model times available in wrfout_dir:")
print(f"{ript.get_model_times(wrfout_dir)}".replace(",", "\n"))

ripdp = ript.preprocess(
    wrfout_dir=wrfout_dir,
    output_dir=output_dir,
    file_tag=file_tag,
    image_path=image_path,
)

print(ripdp)

tp = ript.point_trajectory(
    wrfout_dir=wrfout_dir,
    output_dir=output_dir,
    ripdp_data=ripdp,
    traj_tag="yucatan",
    traj_x=0,
    traj_y=2.3e6,
    traj_z=900,
    traj_t_0=0,
    traj_t_f=9,
    traj_dt=1200,
    hydrometeor=0,
    traj_diagnostics=ript.diagnostic_groups("base"),
    image_path=image_path,
)

print(tp)
