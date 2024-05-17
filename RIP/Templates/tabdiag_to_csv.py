import os
import sys


def tabdiag_to_csv(cwd, tabdiag_file):
    # Get full header
    with open(f"{cwd}/tabdiag_format.in", "r") as f:
        lines = f.readlines()
        header = lines[0].strip().replace("'", "")

    # Get data
    with open(tabdiag_file, "r") as f:
        lines = f.readlines()
        data = []
        for line in lines:
            # skip if empty, or if it contains "===" or "Trajectory" or "Time [h]"
            if (
                not line.strip()
                or "===" in line
                or "Trajectory" in line
                or "Time [h]" in line
            ):
                continue
            else:
                data.append(line.split())

    # Write to csv
    csv_file = f"{cwd}/{os.path.basename(tabdiag_file).replace('.tabdiag', '.csv')}"
    with open(csv_file, "w") as f:
        f.write(header + "\n")
        for row in data:
            f.write(",".join(row) + "\n")


def convert_all_tabdiag_to_csv(cwd, path_to_diag_files="BTrajectories"):
    tabdiag_files = []
    for root, dirs, files in os.walk(path_to_diag_files):
        for file in files:
            if file.endswith(".tabdiag"):
                tabdiag_files.append(os.path.join(root, file))
    for tabdiag_file in tabdiag_files:
        tabdiag_to_csv(cwd, tabdiag_file)


if __name__ == "__main__":
    cwd = os.path.dirname(os.path.abspath(__file__))
    if len(sys.argv) == 2:
        if sys.argv[1] == "all":
            convert_all_tabdiag_to_csv(cwd)
        else:
            if os.path.exists(sys.argv[1]):
                tabdiag_to_csv(cwd, sys.argv[1])
            else:
                print(f"File {sys.argv[1]} does not exist")
    else:
        print("Usage: ")
        print("  To convert all tabdiag files in BTrajectories, use:")
        print("    python tabdiag_to_csv.py all")
        print("  To convert a single tabdiag file, use:")
        print("    python tabdiag_to_csv.py <path_to_tabdiag_file>")
