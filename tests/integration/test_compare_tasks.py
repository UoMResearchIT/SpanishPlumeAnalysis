from pathlib import Path

import pytest
from tests.integration.conftest import assert_valid_mp4
import wrf_analysis_toolkit as wat


def _run_diagnostic(var_name: str, wrf_dir: Path, out_dir: Path) -> None:
    outfile = wat.diagnostic(
        variable_name=var_name,
        wrfout_dir=str(wrf_dir),
        output_dir=str(out_dir),
    )
    assert_valid_mp4(out_dir / f"{outfile}.mp4")


@pytest.fixture()
def prepared_compare_inputs(
    tmp_path: Path, wrf_input_dirs: tuple[Path, Path]
) -> tuple[Path, Path]:
    control_wrf_dir, zero_wrf_dir = wrf_input_dirs
    control_out = tmp_path / "control"
    zero_out = tmp_path / "zero"
    control_out.mkdir(parents=True, exist_ok=True)
    zero_out.mkdir(parents=True, exist_ok=True)

    for var_name in ("DewpointTemp925", "CAPE"):
        _run_diagnostic(var_name, control_wrf_dir, control_out)
        _run_diagnostic(var_name, zero_wrf_dir, zero_out)

    return control_out, zero_out


@pytest.mark.integration
@pytest.mark.slow
def test_wrfcompare_generates_diff_mp4(
    tmp_path: Path, wrf_input_dirs: tuple[Path, Path]
) -> None:
    control_wrf_dir, zero_wrf_dir = wrf_input_dirs
    out_dir = tmp_path / "wrfcompare"
    out_dir.mkdir(parents=True, exist_ok=True)

    outfile = wat.wrfdiff(
        variable_name="DewpointTemp925",
        wrfout_dir_A=str(control_wrf_dir),
        wrfout_dir_B=str(zero_wrf_dir),
        label_diff="Control-Zero",
        output_dir=str(out_dir),
        file_tag="_wrf_diff_control-zero",
    )
    assert_valid_mp4(out_dir / f"{outfile}.mp4")


@pytest.mark.integration
@pytest.mark.slow
def test_mp4diff_generates_comparison_mp4(
    tmp_path: Path, prepared_compare_inputs: tuple[Path, Path]
) -> None:
    control_out, zero_out = prepared_compare_inputs
    out_dir = tmp_path / "mp4diff"
    out_dir.mkdir(parents=True, exist_ok=True)

    outfile = wat.mp4diff(
        file_A=str(control_out / "DewpointTemp925.mp4"),
        file_B=str(zero_out / "DewpointTemp925.mp4"),
        label_A="control",
        label_B="zero",
        label_diff="Control-Zero",
        output_dir=str(out_dir),
        file_tag="_control-zero",
    )
    assert_valid_mp4(out_dir / f"{outfile}.mp4")


@pytest.mark.integration
@pytest.mark.slow
def test_mp4stitch_generates_stitched_mp4(
    tmp_path: Path, prepared_compare_inputs: tuple[Path, Path]
) -> None:
    control_out, zero_out = prepared_compare_inputs
    out_dir = tmp_path / "mp4stitch"
    out_dir.mkdir(parents=True, exist_ok=True)

    outfile = wat.mp4stitch(
        file_paths=[
            str(control_out / "DewpointTemp925.mp4"),
            str(zero_out / "DewpointTemp925.mp4"),
            str(control_out / "CAPE.mp4"),
            str(zero_out / "CAPE.mp4"),
        ],
        rows=2,
        cols=2,
        labels=["control", "zero", "control", "zero"],
        output_dir=str(out_dir),
        file_tag="_mp4_stitch_control-zero",
    )
    stitched = out_dir / outfile
    assert stitched.name.endswith("_mp4_stitch_control-zero.mp4")
    assert_valid_mp4(stitched)
