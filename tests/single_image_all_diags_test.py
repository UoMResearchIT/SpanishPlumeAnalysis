import sys
import os
import glob

src = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(1, src)
import subprocess
from datetime import datetime

import src.SensibleVariables as sv

wrfdata = f"/home/ubuntu/SpanishPlume/tests/wrfdata/control"
results = f"{src}/tests/results"
t0 = datetime.now()
t0_s = t0.strftime("%Y-%m-%d_%H-%M-%S")
results = f"{results}/tsiad_{t0_s}"
output_file = f"{results}/test_single_image_all_diags{t0_s}.pdf"

# Get all diagnostic variables
sens_vars = [
    attr
    for attr in dir(sv)
    if not callable(getattr(sv, attr)) and not attr.startswith("__")
]
diagnostics = [var for var in sens_vars if not var.startswith("SkewT")]
diagnostics.append("SkewT")
print(f"\nGenerating pdf with single image of each diagnostic variable:")
for diag in diagnostics:
    print(f"  - {diag}")

# Run each diagnostic variable
subprocess.run(f"mkdir -p {results}", shell=True)
for diag in diagnostics:
    args = f"--task=diagnostic --var={diag} --dir_path={wrfdata}/ --save_pdf_frames=1 --outdir={results}/"
    ti = datetime.now()
    print(f"\nStarted at: {ti}")
    print(f"\nFinished after: {datetime.now()-ti}")
print(f"\n\nTotal run time: {datetime.now()-t0}")
    print(f"\npython {src}/main.py {args}")
    result = subprocess.run(f"python {src}/main.py {args}", shell=True)

# Combine all PDFs into a single PDF file
print("\n\nCombining all PDFs into a single PDF file")
subprocess.run(["rm", "-f"] + glob.glob(f"{results}/*.mp4"), check=True)
for pdf_file in glob.glob(f"{results}/__*/*.pdf"):
    subprocess.run(["mv", pdf_file, results], check=True)
for dir in glob.glob(f"{results}/__*"):
    subprocess.run(["rm", "-d", dir], check=True)
subprocess.run(
    ["pdfunite"] + glob.glob(f"{results}/*.pdf") + [f"{results}/output.p"], check=True
)
if os.path.exists(f"{results}/output.p"):
    subprocess.run(["rm"] + glob.glob(f"{results}/*.pdf"), check=True)
    subprocess.run(
        ["mv", f"{results}/output.p", output_file],
        check=True,
    )
    subprocess.run(
        ["mv", output_file, f"{results}/.."],
        check=True,
    )
    subprocess.run(["rm", "-d", results], check=True)


print("\n\nDone!")
