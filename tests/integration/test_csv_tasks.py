import csv
from pathlib import Path

import pytest

CSV_DATA_V = ["AirTemp", "DewpointTemp", "RelativeHumidity"]
CSV_DATA_P = [925, 850, 700, 500, 300]
CSV_DATA_SVARS = ["CIN", "CAPE"] + [
    f"{var}{height}" for var in CSV_DATA_V for height in CSV_DATA_P
]


def _expected_csv_columns() -> list[str]:
    from wrf_analysis_toolkit import SensibleVariables as sv

    # CSV columns are based on each sensible variable's outfile name.
    return ["Timestamp"] + [
        getattr(sv, var_name).outfile for var_name in CSV_DATA_SVARS
    ]


def _assert_valid_csv(csv_file: Path, expected_columns: list[str]) -> None:
    assert csv_file.exists(), f"Expected CSV file was not created: {csv_file}"
    assert csv_file.stat().st_size > 0, f"CSV file is empty: {csv_file}"

    with csv_file.open("r", newline="") as f:
        metadata = f.readline().strip()
        assert metadata.startswith(
            "# lat:"
        ), f"CSV metadata header is missing/invalid in {csv_file}: {metadata}"

        reader = csv.reader(f)
        header = next(reader)
        assert header == expected_columns, (
            f"CSV columns mismatch in {csv_file}.\n"
            f"Expected: {expected_columns}\n"
            f"Got: {header}"
        )

        first_data_row = next(reader, None)
        assert first_data_row is not None, f"CSV has no data rows: {csv_file}"
        assert len(first_data_row) == len(expected_columns), (
            f"CSV first data row has wrong width in {csv_file}.\n"
            f"Expected {len(expected_columns)} fields, got {len(first_data_row)}"
        )


@pytest.mark.integration
@pytest.mark.slow
def test_csv_task_from_csv_place_shortcut(
    tmp_path: Path, wrf_control_dir: Path, run_cli
) -> None:
    result = run_cli(
        [
            "--task=csv",
            "--var=CSV_BristolChannel",
            f"--wrfout_dir={wrf_control_dir}",
            f"--output_dir={tmp_path}",
            "--domain=full",
        ]
    )

    assert result.returncode == 0, (
        "csv task failed for CSV_BristolChannel.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

    expected_columns = _expected_csv_columns()
    _assert_valid_csv(tmp_path / "CSV_Data_BristolChannel.csv", expected_columns)


@pytest.mark.integration
@pytest.mark.slow
def test_csv_task_from_explicit_variable_list(
    tmp_path: Path, wrf_control_dir: Path, run_cli
) -> None:
    result = run_cli(
        [
            "--task=csv",
            f"--var={','.join(CSV_DATA_SVARS)}",
            f"--wrfout_dir={wrf_control_dir}",
            f"--output_dir={tmp_path}",
            "--domain=full",
            "--place=Bath",
        ]
    )

    assert result.returncode == 0, (
        "csv task failed for explicit variable list with place=Bath.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

    expected_columns = _expected_csv_columns()
    _assert_valid_csv(tmp_path / "CSV_Data_Bath.csv", expected_columns)
