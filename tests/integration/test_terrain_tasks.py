from pathlib import Path

import pytest
from tests.integration.conftest import (
    assert_valid_pdf,
    terrain_diagnostic_variables,
)

import wrf_analysis_toolkit as wat


@pytest.mark.integration
@pytest.mark.slow
def test_terrain(tmp_path, wrf_control_dir):
    produced_name = wat.terrain(
        wrfout_dir=str(wrf_control_dir),
        output_dir=str(tmp_path),
        domain="full",
    )

    assert f"{produced_name}" == "TerrainElevation"
    assert_valid_pdf(tmp_path / f"{produced_name}.pdf")


def test_terrain_with_point(tmp_path, wrf_control_dir):
    produced_name = wat.terrain(
        wrfout_dir=str(wrf_control_dir),
        output_dir=str(tmp_path),
        domain="UK",
        place="Bath",
        file_tag="_Bath",
    )

    assert f"{produced_name}" == "TerrainElevation_Bath"
    assert_valid_pdf(tmp_path / f"{produced_name}.pdf")
