import sys
import os

src = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(1, src)
import subprocess
from datetime import datetime

wrfdata = f"{src}/tests/wrfdata"
results = f"{src}/tests/results"

csv_data_v = ["AirTemp", "DewpointTemp", "RelativeHumidity"]
csv_data_p = [925, 850, 700, 500, 300]
csv_data_svars = ["CIN", "CAPE"] + [
    f"{var}{height}" for var in csv_data_v for height in csv_data_p
]

all_args = [
    # f"--task=diagnostic --var=TerrainElevation    --dir_path={wrfdata}/control/         --outdir={results}/ --file_tag=_control",
    # f"--task=diagnostic --var=TerrainElevation    --dir_path={wrfdata}/control/         --outdir={results}/ --domain=full --file_tag=_control_full",
    # f"--task=diagnostic --var=TerrainElevation1000    --dir_path={wrfdata}/d02/  --domain=full  --outdir={results}/ --lat=51.38  --lon=-2.36 --file_tag=_Bath",
    # f"--task=diagnostic --var=TerrainElevation1000    --dir_path={wrfdata}/d02/  --domain=full  --outdir={results}/ --lat=51.02 --lon=-5.23 --place=BristolChannel",
    # f"--task=diagnostic --var=TerrainElevation1000    --dir_path={wrfdata}/d02/  --domain=full  --outdir={results}/ --lat=51.64  --lon=-3.30 --file_tag=_Caerphilly",
    # f"--task=csv --var=AirTemp2m,DewpointTemp2m,CIN,CAPE    --dir_path={wrfdata}/d02/  --domain=full  --outdir={results}/ --lat=51.38  --lon=-2.36 --file_tag=_Bath",
    # f"--task=csv --var=CSV_BristolChannel    --dir_path={wrfdata}/d02/  --domain=full  --outdir={results}/",
    # f"--task=csv --var={','.join(csv_data_svars)}    --dir_path={wrfdata}/d02/  --domain=full  --outdir={results}/ --place=Bath",
    # f"--task=csv --var={','.join(csv_data_svars)}    --dir_path={wrfdata}/_zlast_two_control/  --domain=full  --outdir={results}/ --lat=51.38  --lon=-2.36 --file_tag=_bath",
    # f"--task=diagnostic --var=TerrainElevation    --dir_path={wrfdata}/control/         --outdir={results}/ --lat=42.9 --lon=2.43 --domain=full --file_tag=_point_full",
    # f"--task=diagnostic --var=TerrainElevation    --dir_path={wrfdata}/double/          --outdir={results}/ --file_tag=_double",
    # f"--task=diagnostic --var=TerrainElevation    --dir_path={wrfdata}/half/            --outdir={results}/ --file_tag=_half",
    # f"--task=diagnostic --var=TerrainElevation    --dir_path={wrfdata}/zero/            --outdir={results}/ --file_tag=_zero",
    # f"--task=diagnostic --var=TerrainElevation1000    --dir_path={wrfdata}/d02/            --outdir={results}/ --file_tag=_d02_full --domain=full",
    # f"--task=diagnostic   --var=DewpointTemp2m        --dir_path={wrfdata}/control/         --outdir={results}/",
    # f"--task=diagnostic   --var=Rain        --dir_path={wrfdata}/control/         --outdir={results}/ --save_pdf_frames=1",
    # f"--task=diagnostic   --var=AirTemp2m        --dir_path={wrfdata}/control/         --outdir={results}/",
    # f"--task=diagnostic   --var=AirTemp500        --dir_path={wrfdata}/control/         --outdir={results}/",
    # f"--task=diagnostic   --var=AirTemp850        --dir_path={wrfdata}/control/         --outdir={results}/",
    # f"--task=diagnostic   --var=AirTempDif6h850   --dir_path={wrfdata}/_zfirst_control/ --outdir={results}/",
    # f"--task=diagnostic   --var=AirTempDif6h700   --dir_path={wrfdata}/_zfirst_control/ --outdir={results}/",
    # f"--task=diagnostic   --var=AirTempDif6h500   --dir_path={wrfdata}/_zfirst_control/ --outdir={results}/",
    # f"--task=diagnostic   --var=AirTempDif12h850  --dir_path={wrfdata}/_zfirst_control/ --outdir={results}/",
    # f"--task=diagnostic   --var=AirTempDif12h700  --dir_path={wrfdata}/_zfirst_control/ --outdir={results}/",
    # f"--task=diagnostic   --var=AirTempDif12h500  --dir_path={wrfdata}/_zfirst_control/ --outdir={results}/",
    # f"--task=diagnostic   --var=CIN  --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=CIN_YlGnBu --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=CIN_YlGn --dir_path={wrfdata}/control/ --outdir={results}/ --save_pdf_frames=1",
    # f"--task=diagnostic   --var=GeoPotHeight500 --dir_path={wrfdata}/control/ --outdir={results}/ --save_pdf_frames=1",
    # f"--task=diagnostic   --var=RelativeHumidity2m --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=PotentialTemp2m   --dir_path={wrfdata}/control/         --outdir={results}/",
    # f"--task=diagnostic   --var=PotentialTemp925  --dir_path={wrfdata}/control/         --outdir={results}/",
    # f"--task=diagnostic   --var=PotentialTemp850  --dir_path={wrfdata}/_zfirst_control/ --outdir={results}/",
    # f"--task=diagnostic   --var=PotentialTemp800  --dir_path={wrfdata}/control/         --outdir={results}/",
    # f"--task=diagnostic   --var=PotentialTemp700  --dir_path={wrfdata}/control/         --outdir={results}/",
    # f"--task=diagnostic   --var=PotentialTemp600  --dir_path={wrfdata}/control/         --outdir={results}/",
    # f"--task=diagnostic   --var=PotentialTemp500  --dir_path={wrfdata}/control/         --outdir={results}/",
    # f"--task=diagnostic   --var=SeaLevelPressure     --dir_path={wrfdata}/control/         --outdir={results}/ --save_pdf_frames=1 --windbarbs=0",
    # f"--task=diagnostic   --var=SeaLevelPressure1hPa --dir_path={wrfdata}/control/         --outdir={results}/",
    # f"--task=diagnostic   --var=SeaLevelPressure2hPa --dir_path={wrfdata}/control/         --outdir={results}/",
    # f"--task=diagnostic   --var=StaticStability700500  --dir_path={wrfdata}/control/         --outdir={results}/",
    # f"--task=diagnostic   --var=StaticStability850700  --dir_path={wrfdata}/control/         --outdir={results}/",
    # f"--task=diagnostic   --var=Frontogenesis925  --dir_path={wrfdata}/control/         --outdir={results}/",
    # f"--task=diagnostic   --var=Frontogenesis850  --dir_path={wrfdata}/_zfirst_control/ --outdir={results}/",
    # f"--task=diagnostic   --var=Frontogenesis700  --dir_path={wrfdata}/control/         --outdir={results}/",
    # f"--task=diagnostic   --var=Frontogenesis500  --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=SkewT  --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=SkewT  --dir_path={wrfdata}/control/ --outdir={results}/ --lat=42.9 --lon=2.43",
    # f"--task=diagnostic   --var=SkewT_Casablanca   --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=SkewT_Algeria      --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=SkewT_Lerwick      --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=SkewT_Stornoway    --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=SkewT_Nottingham   --dir_path={wrfdata}/control/ --outdir={results}/ --save_pdf_frames=1",
    # f"--task=diagnostic   --var=SkewT_Aberporth    --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=SkewT_LARKHILL     --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=SkewT_Camborne     --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=SkewT_Herstmonceux --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=SkewT_Trappes      --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=SkewT_Bordeaux     --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=SkewT_Nimes        --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=SkewT_La_Coruna    --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=SkewT_Santander    --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=SkewT_Madrid       --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=SkewT_Murcia       --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=SkewT_GIBRALTAR    --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic   --var=InstRain    --dir_path={wrfdata}/control/  --domain=UK  --outdir={results}/ --save_pdf_frames=1",
    # f"--task=diagnostic   --var=SkewT_Trajectory --traj='tests/results/rip/Notin_850hPa.csv'   --dir_path={wrfdata}/_zlast_two_control/ --outdir={results}/ --save_pdf_frames=1",
    # f"--task=diagnostic   --var=AbsoluteVorticity850     --dir_path={wrfdata}/control/         --outdir={results}/ --save_pdf_frames=1",
    # f"--task=diagnostic   --var=Wetbulb850     --dir_path={wrfdata}/control         --outdir={results}/ --save_pdf_frames=1",
    f"--task=diagnostic   --var=GeoPotHeight300     --dir_path={wrfdata}/control         --outdir={results}/ --save_pdf_frames=1",
]
# Append location maps to all_args
# import SensibleVariables as sv
#
# for place in [attr.split("_")[1] for attr in dir(sv) if attr.startswith("SkewT_")]:
#     print(place)
#     all_args.append(
#         f"--task=diagnostic --var=TerrainElevation --dir_path={wrfdata}/control/ --outdir={results}/ --place={place} --file_tag=_{place}"
#     )

t0 = datetime.now()

for args in all_args:
    outdir = args.split("--outdir=")[1]
    if " " in outdir:
        outdir = outdir.split(" ")[0]
    subprocess.run(f"mkdir -p {outdir}", shell=True)
    ti = datetime.now()
    print(f"\nStarted at: {ti}")
    print(f"\npython {src}/CSF/csf.py {args}")
    subprocess.run(f"python {src}/CSF/csf.py {args}", shell=True)
    print(f"\nFinished after: {datetime.now()-ti}")

print(f"\n\nTotal run time: {datetime.now()-t0}")

## RIP
# t0=datetime.now()
# print(f"\nStarted at: {t0}")
## Run these commands from the src directory.
# ./RIP/singularity_rip.sh -od='tests/results/rip' -wd='tests/wrfdata/control/' -nt -np
# ./RIP/singularity_rip.sh -od='tests/results/rip' -wd='tests/wrfdata/_zfirst_control/' -nt -np --t_0=0 --t_f=5 --dt=1
# ./RIP/singularity_rip.sh -od='tests/results/rip' --noRDP --trajtimes=5-3 --trajplot='Traj_5'
# ./RIP/singularity_rip.sh -od='tests/results/rip/' --noRDP --trajinputs='tests/results/rip/my_traj_inputs_file' --trajplot='tp_my_inputs' -np
# ./RIP/singularity_rip.sh -od='tests/results/rip/' --noRDP --trajinputs='tests/results/rip/my_traj_inputs_file' --trajplot='tp_my_inputs' -nt
# ./RIP/singularity_rip.sh -pd='tests/results/rip/RIPDP/rdp_rip' -od='tests/results/riptraj/' --trajtimes=1-3

## Or you can try using these... but I think the rpdp does not work called from here for some reason...
# subprocess.run(f"{src}/RIP/singularity_rip.sh -od='{results}/rip' -wd='{wrfdata}/control/' -nt -np",shell=True)
# subprocess.run(f"{src}/RIP/singularity_rip.sh -od='{results}/rip' -wd='{wrfdata}/_zfirst_control/' -nt -np --t_0=0 --t_f=5 --dt=1",shell=True)
# subprocess.run(f"{src}/RIP/singularity_rip.sh -od='{results}/rip' --noRDP --trajtimes=5-3 --trajplot='Traj_5'",shell=True)
# with open(f"{results}/rip/my_traj_inputs_file", 'w') as file:
#     file.write(
#         """#traj_t_0 traj_t_f traj_dt file_dt traj_x traj_y traj_p hydrometeor color
# 5         2        600     3600    190    400    900    0           red
# 1         4        600     3600    100    250    750    0           blue
# """)
# subprocess.run(f"{src}/RIP/singularity_rip.sh -od='{results}/rip' --noRDP --trajinputs='{results}/rip/my_traj_inputs_file' --trajplot='tp_my_inputs' -np -i",shell=True)
# subprocess.run(f"{src}/RIP/singularity_rip.sh -od='{results}/rip' --noRDP --trajinputs='{results}/rip/my_traj_inputs_file' --trajplot='tp_my_inputs' -nt",shell=True)
# print(f"\n\nTotal run time: {datetime.now()-t0}")
