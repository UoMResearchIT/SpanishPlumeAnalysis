import subprocess

src="/".join(__file__.split("/")[:-2])
wrfdata=f"{src}/tests/wrfdata"
results=f"{src}/tests/results"

all_args=[
    # f"--task=diagnostic --var=TerrainElevation --dir_path={wrfdata}/control/ --outdir={results}/ --file_tag=_control",
    # f"--task=diagnostic --var=TerrainElevation --dir_path={wrfdata}/double/ --outdir={results}/ --file_tag=_double",
    # f"--task=diagnostic --var=TerrainElevation --dir_path={wrfdata}/half/ --outdir={results}/ --file_tag=_half",
    # f"--task=diagnostic --var=TerrainElevation --dir_path={wrfdata}/zero/ --outdir={results}/ --file_tag=_zero",
    # f"--task=diagnostic --var=AirTemp500 --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic --var=AirTemp850Dif6h --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic --var=AirTemp700Dif6h --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic --var=AirTemp500Dif6h --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic --var=AirTemp850Dif12h --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic --var=AirTemp700Dif12h --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic --var=AirTemp500Dif12h --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic --var=PotentialTemp2m --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic --var=PotentialTemp925 --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic --var=PotentialTemp850 --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic --var=PotentialTemp800 --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic --var=PotentialTemp700 --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic --var=PotentialTemp600 --dir_path={wrfdata}/control/ --outdir={results}/",
    # f"--task=diagnostic --var=PotentialTemp500 --dir_path={wrfdata}/control/ --outdir={results}/",
    ]

for args in all_args:
    outdir=args.split("--outdir=")[1]
    if " " in outdir:
        outdir = outdir.split(" ")[0]
    subprocess.run(f"mkdir -p {outdir}",shell=True)
    subprocess.run(f"python {src}/CSF/csf.py {args}",shell=True)

