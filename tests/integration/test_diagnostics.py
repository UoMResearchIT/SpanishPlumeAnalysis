import shutil
from pathlib import Path

import pytest
from tests.integration.conftest import (
    assert_valid_mp4,
    assert_valid_pdf,
    non_terrain_diagnostic_variables,
)

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
def test_generate_single_image_for_diagnostic(
    diag: str,
    tmp_path: Path,
    wrf_control_dir: Path,
    total_timesteps: int,
    run_cli,
) -> None:
    min_timesteps = _diag_needs_timesteps(diag)
    if total_timesteps < min_timesteps:
        pytest.skip(
            f"{diag} needs at least {min_timesteps} timesteps; dataset has {total_timesteps}."
        )

    print(f"...", flush=True)
    print(f"    ", end="")

    result = run_cli(
        [
            "--task=diagnostic",
            f"--var={diag}",
            f"--dir_path={wrf_control_dir}",
            f"--outdir={tmp_path}",
            "--save_pdf_frames=1",
        ]
    )

    assert result.returncode == 0, (
        f"Diagnostic run failed for {diag}\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

    from src import SensibleVariables as sv

    outfile_stem = getattr(sv, diag).outfile

    mp4_file = tmp_path / f"{outfile_stem}.mp4"
    assert_valid_mp4(mp4_file)

    pdf_dir = tmp_path / f"__{outfile_stem}"
    pdf_files = sorted(pdf_dir.glob("*.pdf"))
    assert pdf_files, (
        f"No PDF frames generated for {diag}. Expected files in {pdf_dir}.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )
    assert_valid_pdf(pdf_files[0])

    # Keep resource usage bounded across many parametrized diagnostics.
    mp4_file.unlink(missing_ok=True)
    shutil.rmtree(pdf_dir, ignore_errors=True)
