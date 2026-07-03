import shutil
from pathlib import Path

import pytest
from tests.integration.conftest import (
    assert_valid_mp4,
    assert_valid_pdf,
    non_terrain_diagnostic_variables,
)

import wrf_analysis_toolkit as wat

# Optional manual curation template.
# Leave empty to test all available diagnostics discovered from SensibleVariables.
# Example:
# EXPECTED_DIAGNOSTICS = ["DewpointTemp925", "CAPE", "SkewT"]
EXPECTED_DIAGNOSTICS: list[str] = []


def _selected_diagnostics() -> list[str]:
    diagnostics = non_terrain_diagnostic_variables()
    if not EXPECTED_DIAGNOSTICS:
        return diagnostics

    missing = [d for d in EXPECTED_DIAGNOSTICS if d not in diagnostics]
    assert not missing, "EXPECTED_DIAGNOSTICS contains unknown variables: " + ", ".join(
        missing
    )
    return EXPECTED_DIAGNOSTICS


def _diag_needs_timesteps(diag: str) -> int:
    if "AirTempDif12h" in diag:
        return 13
    if "AirTempDif6h" in diag:
        return 7
    return 1


@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.parametrize("diag", _selected_diagnostics(), ids=lambda d: f"{d}")
def test_diagnostic(
    diag: str, tmp_path: Path, wrf_control_dir: Path, total_timesteps: int
) -> None:
    min_timesteps = _diag_needs_timesteps(diag)
    if total_timesteps < min_timesteps:
        pytest.skip(
            f"{diag} needs at least {min_timesteps} timesteps; dataset has {total_timesteps}."
        )

    print(f"...", flush=True)
    print(f"    ", end="")

    produced_name = wat.diagnostic(
        variable_name=diag,
        wrfout_dir=str(wrf_control_dir),
        output_dir=str(tmp_path),
        save_pdf_frames=True,
    )

    from wrf_analysis_toolkit import SensibleVariables as sv

    outfile_stem = getattr(sv, diag).outfile
    assert produced_name == outfile_stem

    mp4_file = tmp_path / f"{outfile_stem}.mp4"
    assert_valid_mp4(mp4_file)

    pdf_dir = tmp_path / f"__{outfile_stem}"
    pdf_files = sorted(pdf_dir.glob("*.pdf"))
    assert (
        pdf_files
    ), f"No PDF frames generated for {diag}. Expected files in {pdf_dir}."
    assert_valid_pdf(pdf_files[0])

    # Keep resource usage bounded across many parametrized diagnostics.
    mp4_file.unlink(missing_ok=True)
    shutil.rmtree(pdf_dir, ignore_errors=True)


def test_terrain_diagnostic_redirects(wrf_control_dir: Path, tmp_path: Path) -> None:
    diag = "TerrainElevation"
    produced_name = wat.diagnostic(
        variable_name=diag,
        wrfout_dir=str(wrf_control_dir),
        output_dir=str(tmp_path),
    )

    from wrf_analysis_toolkit import SensibleVariables as sv

    outfile_stem = getattr(sv, diag).outfile
    assert produced_name == outfile_stem

    assert_valid_pdf(tmp_path / f"{outfile_stem}.pdf")

    # Terrain diagnostics should be redirected and not produce mp4/pdf frame dir artifacts.
    assert not (tmp_path / f"{outfile_stem}.mp4").exists()
    assert not (tmp_path / f"__{outfile_stem}").exists()
