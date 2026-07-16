import rip_toolkit as ript

wrfout_dir = "RIP_legacy/Sample/WRFData"
output_dir = "tests/integration/results"
file_tag = "test"
image_path = "RIP_legacy/ripdocker_latest.sif"

ripdp = ript.preprocess(
    wrfout_dir=wrfout_dir,
    output_dir=output_dir,
    file_tag=file_tag,
    image_path=image_path,
)

print(ripdp)
