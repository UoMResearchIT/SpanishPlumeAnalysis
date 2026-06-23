import sys
import os

base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(1, base_dir)
import subprocess
from datetime import datetime

wrfdata_path = f"/home/ubuntu/SpanishPlume/tests/wrfdata/control"
res_path = f"{base_dir}/tests/results"

csv_data_v = ["AirTemp", "DewpointTemp", "RelativeHumidity"]
csv_data_p = [925, 850, 700, 500, 300]
csv_data_svars = ["CIN", "CAPE"] + [
    f"{var}{height}" for var in csv_data_v for height in csv_data_p
]

all_args = [
    f"--task=diagnostic   --var=DewpointTemp2m              --dir_path={wrfdata_path}/      --outdir={res_path}/",
    f"--task=diagnostic   --var=CAPE                        --dir_path={wrfdata_path}/      --outdir={res_path}/ --save_pdf_frames=1",
    f"--task=diagnostic   --var=TerrainElevation1000        --dir_path={wrfdata_path}/      --outdir={res_path}/ --file_tag=_full --domain=full",
    f"--task=diagnostic   --var=TerrainElevation            --dir_path={wrfdata_path}/      --outdir={res_path}/ --lat=42.9 --lon=2.43 --domain=full --file_tag=_point_full",
    f"--task=diagnostic   --var=TerrainElevation1000        --dir_path={wrfdata_path}/      --outdir={res_path}/ --domain=full --lat=51.38  --lon=-2.36 --file_tag=_Bath1",
    f"--task=csv          --var=CSV_BristolChannel          --dir_path={wrfdata_path}/      --outdir={res_path}/ --domain=full",
    f"--task=csv          --var={','.join(csv_data_svars)}  --dir_path={wrfdata_path}/      --outdir={res_path}/ --domain=full --place=Bath",
    f"--task=csv          --var={','.join(csv_data_svars)}  --dir_path={wrfdata_path}/      --outdir={res_path}/ --domain=full --lat=51.38  --lon=-2.36 --file_tag=_bath",
]


big_div = "\n" + "=" * 80 + "\n"
print(big_div)

t0 = datetime.now()

for args in all_args:
    outdir = args.split("--outdir=")[1]
    if " " in outdir:
        outdir = outdir.split(" ")[0]
    subprocess.run(f"mkdir -p {outdir}", shell=True)
    ti = datetime.now()
    print(f"\n--------------- Started at: {ti}")
    print(f"\npython {base_dir}/main.py {args}")
    subprocess.run(f"python {base_dir}/main.py {args}", shell=True)
    print(f"\n--------------- Finished after: {datetime.now()-ti}")

print(f"\n\nTotal run time: {datetime.now()-t0}")

print(big_div)
