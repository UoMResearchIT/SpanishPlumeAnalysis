from pathlib import Path

import pytest
from tests.integration.conftest import assert_valid_mp4


def _run_diagnostic(var_name: str, wrf_dir: Path, out_dir: Path, run_cli) -> None:
    result = run_cli(
        [
            "--task=diagnostic",
            f"--var={var_name}",
            f"--dir_path={wrf_dir}",
            f"--outdir={out_dir}",
        ]
    )
    assert result.returncode == 0, (
        f"Failed to generate prerequisite diagnostic {var_name}.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

@pytest.fixture()
def prepared_compare_inputs(
    tmp_path: Path, wrf_input_dirs: tuple[Path, Path], run_cli
) -> tuple[Path, Path]:
    control_wrf_dir, zero_wrf_dir = wrf_input_dirs
    control_out = tmp_path / "control"
    zero_out = tmp_path / "zero"
    control_out.mkdir(parents=True, exist_ok=True)
    zero_out.mkdir(parents=True, exist_ok=True)

    for var_name in ("DewpointTemp925", "CAPE"):
        _run_diagnostic(var_name, control_wrf_dir, control_out, run_cli)
        _run_diagnostic(var_name, zero_wrf_dir, zero_out, run_cli)

    return control_out, zero_out


@pytest.mark.integration
@pytest.mark.slow
def test_wrfcompare_generates_diff_mp4(
    tmp_path: Path, wrf_input_dirs: tuple[Path, Path], run_cli
) -> None:
    control_wrf_dir, zero_wrf_dir = wrf_input_dirs
    out_dir = tmp_path / "wrfcompare"
    out_dir.mkdir(parents=True, exist_ok=True)

    result = run_cli(
        [
            "--task=wrfcompare",
            "--var=DewpointTemp925",
            f"--dir1={control_wrf_dir}",
            f"--dir2={zero_wrf_dir}",
            "--difflabel=Control-Zero",
            f"--outdir={out_dir}",
            "--file_tag=_wrf_diff_control-zero",
        ]
    )

    assert result.returncode == 0, (
        "wrfcompare task failed.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

    assert_valid_mp4(out_dir / "DewpointTemp925_wrf_diff_control-zero.mp4")


@pytest.mark.integration
@pytest.mark.slow
def test_mp4diff_generates_comparison_mp4(
    tmp_path: Path, prepared_compare_inputs: tuple[Path, Path], run_cli
) -> None:
    control_out, zero_out = prepared_compare_inputs
    out_dir = tmp_path / "mp4diff"
    out_dir.mkdir(parents=True, exist_ok=True)

    result = run_cli(
        [
            "--task=mp4diff",
            "--var=DewpointTemp925",
            f"--dir1={control_out}",
            f"--dir2={zero_out}",
            "--label1=control",
            "--label2=zero",
            "--difflabel=Control-Zero",
            f"--outdir={out_dir}",
            "--file_tag=_mp4_diff_control-zero",
        ]
    )

    assert result.returncode == 0, (
        "mp4diff task failed.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

    assert_valid_mp4(out_dir / "DewpointTemp925_mp4_diff_control-zero.mp4")


@pytest.mark.integration
@pytest.mark.slow
def test_mp4stitch_generates_stitched_mp4(
    tmp_path: Path, prepared_compare_inputs: tuple[Path, Path], run_cli
) -> None:
    control_out, zero_out = prepared_compare_inputs
    out_dir = tmp_path / "mp4stitch"
    out_dir.mkdir(parents=True, exist_ok=True)

    result = run_cli(
        [
            "--task=mp4stitch",
            "--files=DewpointTemp925,DewpointTemp925,CAPE,CAPE",
            f"--dirs={control_out},{zero_out},{control_out},{zero_out}",
            "--M=2",
            "--N=2",
            "--labels=control,zero,control,zero",
            f"--outdir={out_dir}",
            "--file_tag=_mp4_stitch_control-zero",
        ]
    )

    assert result.returncode == 0, (
        "mp4stitch task failed.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

    produced_mp4s = sorted(out_dir.glob("*.mp4"))
    assert len(produced_mp4s) == 1, (
        "Expected exactly one stitched MP4 in output directory. "
        f"Found: {[p.name for p in produced_mp4s]}"
    )
    assert produced_mp4s[0].name.endswith("_mp4_stitch_control-zero.mp4")
    assert_valid_mp4(produced_mp4s[0])
