from pathlib import Path

import pytest
from tests.integration.conftest import (
    assert_valid_pdf,
    terrain_diagnostic_variables,
)


def _terrain_cases() -> list[tuple[list[str], str, bool]]:
    cases: list[tuple[list[str], str, bool]] = []
    terrain_diags = set(terrain_diagnostic_variables())

    if "TerrainElevation" in terrain_diags:
        cases.append(
            (
                [
                    "--task=diagnostic",
                    "--var=TerrainElevation",
                    "--domain=full",
                ],
                "TerrainElevation.pdf",
                False,
            )
        )
    # Add a test case with a point annotation at Bath (51.38, -2.36)
    if "TerrainElevation1000" in terrain_diags:
        cases.append(
            (
                [
                    "--task=diagnostic",
                    "--var=TerrainElevation1000",
                    "--domain=full",
                    "--lat=51.38",
                    "--lon=-2.36",
                    "--file_tag=_Bath1",
                ],
                "TerrainElevation_Bath1.pdf",
                True,
            )
        )

    return cases


TERRAIN_CASES = _terrain_cases()
TERRAIN_CASE_IDS = [
    output_name.replace(".pdf", "") for _, output_name, _ in TERRAIN_CASES
]


@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.parametrize(
    "cli_args, output_name, expect_point_log",
    TERRAIN_CASES,
    ids=TERRAIN_CASE_IDS,
)
def test_terrain_diagnostics_generate_expected_pdf(
    tmp_path: Path,
    wrf_control_dir: Path,
    cli_args: list[str],
    output_name: str,
    expect_point_log: bool,
    run_cli,
) -> None:
    result = run_cli(
        [
            *cli_args,
            f"--wrfout_dir={wrf_control_dir}",
            f"--output_dir={tmp_path}",
        ]
    )

    assert result.returncode == 0, (
        "terrain diagnostic task with point annotation failed.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

    if expect_point_log:
        assert "Adding point to map at:" in result.stdout, (
            "Terrain point annotation path was not executed.\n"
            f"STDOUT:\n{result.stdout}"
        )

    assert_valid_pdf(tmp_path / output_name)
