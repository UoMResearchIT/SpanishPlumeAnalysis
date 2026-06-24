import sys
import os
import glob

base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(1, base_dir)
import subprocess
from datetime import datetime

import src.SensibleVariables as sv

wrfdata = f"/home/ubuntu/SpanishPlume/tests/wrfdata/control"
results = f"{base_dir}/tests/results"
t0 = datetime.now()
t0_s = t0.strftime("%Y-%m-%d_%H-%M-%S")
results = f"{results}/tsiad_{t0_s}"
output_file = f"{results}/test_single_image_all_diags{t0_s}.pdf"

big_div = "\n" + "=" * 80 + "\n"
print(big_div)

# Get all diagnostic variables
sens_vars = sv.get_sv_names()
diagnostics = [var for var in sens_vars if not var.startswith("SkewT")]
diagnostics.append("SkewT")
print(f"\nGenerating pdf with single image of each diagnostic variable:")
for diag in diagnostics:
    print(f"  - {diag}")

# Run each diagnostic variable
print(big_div)
diag_status = {d: {"exit": "Not Run", "runtime": "---"} for d in diagnostics}
subprocess.run(f"mkdir -p {results}", shell=True)
for diag in diagnostics:
    args = f"--task=diagnostic --var={diag} --dir_path={wrfdata}/ --save_pdf_frames=1 --outdir={results}/"
    ti = datetime.now()
    print(f"\n----- {diag} ---------- Started at: {ti}")
    print(f"\npython {base_dir}/main.py {args}")
    result = subprocess.run(f"python {base_dir}/main.py {args}", shell=True)
    runtime = datetime.now() - ti
    print(f"\n----- {diag} ---------- Finished after: {runtime}")
    diag_status[diag] = {
        "exit": "OK" if result.returncode == 0 else "ERROR",
        "runtime": runtime,
    }

print(big_div)
print("\n\nDiagnostic generation done. Status summary:")
diag_label_width = max(len(diag) for diag in diagnostics) + 4
exit_label_width = max(len(status["exit"]) for status in diag_status.values()) + 2
for diag, status in diag_status.items():
    print(
        f"  - {diag.ljust(diag_label_width)}{status['exit'].ljust(exit_label_width)} finished in   {status['runtime']}"
    )
print(f"\n\n  Total run time: {datetime.now()-t0}")

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
print(big_div)
