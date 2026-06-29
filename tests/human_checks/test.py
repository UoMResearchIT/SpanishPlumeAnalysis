# This script runs main in a cli and passes the arguments in all_args.
# It is meant to generate sample outputs, for a human to check.
# Run this script with:
# ```
# export WRF_DATA_PATH=/path/to/wrfdata
# python ./test.py
# ```

import sys
import os

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.insert(1, base_dir)
import subprocess
from datetime import datetime

wrfdata = os.getenv("WRF_DATA_PATH", "/wrfdata")
wrfdata = wrfdata[:-1] if wrfdata.endswith("/") else wrfdata
res_path = os.getenv("RESULTS_PATH", f"{base_dir}/tests/human_checks/results")

csv_data_v = ["AirTemp", "DewpointTemp", "RelativeHumidity"]
csv_data_p = [925, 850, 700, 500, 300]
csv_data_svars = ["CIN", "CAPE"] + [
    f"{var}{height}" for var in csv_data_v for height in csv_data_p
]

all_args = [
    f"--task=diagnostic   --var=DewpointTemp925              --dir_path={wrfdata}/control/      --outdir={res_path}/control/",
    f"--task=diagnostic   --var=DewpointTemp925              --dir_path={wrfdata}/zero/         --outdir={res_path}/zero/",
    f"--task=diagnostic   --var=CAPE                         --dir_path={wrfdata}/control/      --outdir={res_path}/control/ --save_pdf_frames=1",
    f"--task=diagnostic   --var=CAPE                         --dir_path={wrfdata}/control/      --outdir={res_path}/zero/",
    f"--task=diagnostic   --var=TerrainElevation1000        --dir_path={wrfdata}/control/      --outdir={res_path}/ --domain=full --lat=51.38  --lon=-2.36 --file_tag=_Bath1",
    f"--task=csv          --var=CSV_BristolChannel          --dir_path={wrfdata}/control/      --outdir={res_path}/ --domain=full",
    f"--task=csv          --var={','.join(csv_data_svars)}  --dir_path={wrfdata}/control/      --outdir={res_path}/ --domain=full --place=Bath",
    f"--task=wrfcompare   --var=DewpointTemp925  --dir1={wrfdata}/control/ --dir2={wrfdata}/zero/ --difflabel=Control-Zero --outdir={res_path}/ --file_tag=_wrf_diff_control-zero",
    f"--task=mp4diff      --var=DewpointTemp925  --dir1={res_path}/control/ --dir2={res_path}/zero/ --label1=control --label2=zero --difflabel=Control-Zero --outdir={res_path}/ --file_tag=_mp4_diff_control-zero",
    f"--task=mp4stitch    --files=DewpointTemp925,DewpointTemp925,CAPE,CAPE --dirs={res_path}/control/,{res_path}/zero/,{res_path}/control/,{res_path}/zero/ --M=2 --N=2 --labels=control,zero,control,zero --outdir={res_path}/ --file_tag=_mp4_stitch_control-zero",
]


big_div = "\n" + "=" * 80 + "\n"
print(big_div)

tasks = []
for arg in all_args:
    t = arg.split("--task=")[1].split(" ")[0]
    var = arg.split("--var=")[1].split(" ")[0] if "--var=" in arg else ""
    var = var[:30] + "..." if len(var) > 30 else var
    tag = arg.split("--file_tag=")[1].split(" ")[0] if "--file_tag=" in arg else ""
    task = f"{t}_{var}{tag}"
    task = task.replace(",", "-")
    tasks.append(task)

task_status = {d: {"exit": "Not Run", "runtime": "---"} for d in tasks}
print(f"\nTasks:")
for task in tasks:
    print(f"  - {task}")

t0 = datetime.now()

for args, task in zip(all_args, tasks):
    outdir = args.split("--outdir=")[1]
    if " " in outdir:
        outdir = outdir.split(" ")[0]
    subprocess.run(f"mkdir -p {outdir}", shell=True)
    ti = datetime.now()
    print(f"\n----- {task} ---------- Started at: {ti}")
    print(f"\npython {base_dir}/main.py {args}")
    result = subprocess.run(f"python {base_dir}/main.py {args}", shell=True)
    runtime = datetime.now() - ti
    print(f"\n----- {task} ---------- Finished after: {runtime}")
    task_status[task] = {
        "exit": "OK" if result.returncode == 0 else "ERROR",
        "runtime": runtime,
    }

print(big_div)
print("\n\nDiagnostic generation done. Status summary:")
task_label_width = max(len(task) for task in tasks) + 4
exit_label_width = max(len(status["exit"]) for status in task_status.values()) + 2
for task, status in task_status.items():
    print(
        f"  - {task.ljust(task_label_width)}{status['exit'].ljust(exit_label_width)} finished in   {status['runtime']}"
    )
print(f"\n\n  Total run time: {datetime.now()-t0}")

print(big_div)
