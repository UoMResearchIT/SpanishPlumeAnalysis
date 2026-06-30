import os
from copy import deepcopy
from typing import List

from wrf_analysis_toolkit.utils import set_variable

import wrf_analysis_toolkit.SensibleVariables as sv
from wrf_analysis_toolkit.Animate import Animate
from wrf_analysis_toolkit.TerrainPlots import Terrain
from wrf_analysis_toolkit.CSV_Data import CSV_Data


def diagnostic(
    wrfout_dir: str,
    output_dir: str,
    variable_name: str,
    file_tag: str = "",
    range_min=None,
    range_max=None,
    windbarbs=None,
    place=None,
    lat=None,
    lon=None,
    trajectory=None,
    domain: str = "zoom",
    smooth: bool = False,
    clean_png_frames: bool = True,
    save_pdf_frames: bool = False,
):
    """
    Generates a diagnostic animation for the specified variable and saves it to the output directory.

    Inputs marked as '(optional)' take default values as defined in SensibleVariables.

    Inputs:
    - wrfout_dir: Directory containing WRF output files.
    - output_dir: Directory where the output file(s) will be saved.
    - variable_name: Name of the variable to analyze (must be defined in SensibleVariables).
    - file_tag: String to append to the output filename (optional).
    - range_min: Minimum value for the variable range (optional).
    - range_max: Maximum value for the variable range (optional).
    - windbarbs: Boolean indicating whether to include wind barbs in the plots (optional).

    For SkewT plots, the following additional inputs are available:
        - place: Predefined location name for SkewT plots (optional).
        - lat: Latitude for the variable (optional). If provided, lon must also be provided.
        - lon: Longitude for the variable (optional). If provided, lat must also be provided.
        - trajectory: Path to a trajectory file for SkewT plots animated along a trajectory (optional).

    - domain: Domain for the plots (default is "zoom").
    - smooth: Boolean indicating whether to apply smoothing to the plots (default is False).
    - clean_png_frames: Boolean indicating whether to delete intermediate PNG frames after creating the animation (default is True).
    - save_pdf_frames: Boolean indicating whether to save each frame as a PDF (default is False).

    Returns: The name of the output file saved in the output directory.
    """
    if "Terrain" in variable_name:
        return terrain(
            wrfout_dir=wrfout_dir,
            output_dir=output_dir,
            variable_name=variable_name,
            file_tag=file_tag,
            range_min=range_min,
            range_max=range_max,
            place=place,
            lat=lat,
            lon=lon,
            domain=domain,
            smooth=smooth,
        )

    svar = set_variable(
        variable_name=variable_name,
        range_min=range_min,
        range_max=range_max,
        windbarbs=windbarbs,
        place=place,
        lat=lat,
        lon=lon,
        trajectory=trajectory,
    )

    outfile = svar.outfile + file_tag

    Animate(
        dir_path=wrfout_dir,
        svariable=svar,
        windbarbs=svar.windbarbs,
        outfile=outfile,
        outdir=output_dir,
        smooth=smooth,
        domain=domain,
        cleanpng=clean_png_frames,
        save_pdf=save_pdf_frames,
    )

    return outfile


def terrain(
    wrfout_dir: str,
    output_dir: str,
    output_format: str = "pdf",
    variable_name: str = "TerrainElevation",
    file_tag: str = "",
    range_min=None,
    range_max=None,
    place=None,
    lat=None,
    lon=None,
    domain: str = "zoom",
    smooth: bool = False,
):
    """
    Generates static image of the terrain elevation in the wrf data and saves it to the output directory.

    Inputs:
    - wrfout_dir: Directory containing WRF output files.
    - output_dir: Directory where the output file(s) will be saved.
    - output_format: Format of the output file (default is "pdf"; can be "png").
    - variable_name: Name of the variable to analyze (must be a TerrainElevation).
    - file_tag: String to append to the output filename (optional).
    - range_min: Minimum value for the elevation range (default is 0). Must be >= 0.
    - range_max: Maximum value for the elevation range (default is 2000). Must be >= 10.
    - domain: Domain for the plot (default is "zoom").
    - smooth: Boolean indicating whether to apply smoothing to the plot (default is False).

    A point can also be added to the plot if lat and lon are provided, or a place if place is provided.
        - place: Predefined location name (optional).
        - lat: Latitude for the variable (optional). If provided, lon must also be provided.
        - lon: Longitude for the variable (optional). If provided, lat must also be provided.

    Returns: The name of the output file saved in the output directory.
    """
    svar = set_variable(
        variable_name=variable_name,
        place=place,
        lat=lat,
        lon=lon,
    )
    # Set elevation range if specified (negative values are not allowed)
    if range_min is not None and range_max is not None:
        range_min = max(float(range_min), 0.0)
        range_max = max(float(range_max), 10.0)

        interval = (range_max - range_min) / 10
        bounds = [range_min - 0.05] + [range_min + i * interval for i in range(0, 11)]
        if range_min == 0:
            bounds[1] = 1

        svar.range_min = range_min
        svar.range_max = range_max
        svar.bounds = bounds

    outfile = svar.outfile + file_tag

    Terrain(
        dir_path=wrfout_dir,
        svariable=svar,
        outfile=outfile,
        outdir=output_dir,
        out_format=output_format,
        smooth=smooth,
        domain=domain,
    )

    return outfile


def csv(
    wrfout_dir: str,
    output_dir: str,
    variable_names: List[str] = None,
    place=None,
    lat=None,
    lon=None,
    file_tag: str = "",
    domain: str = "zoom",
):
    """
    Generates a CSV file with the values of the specified variables at a given location and saves it to the output directory.
    The variables default to AirTemp, DewpointTemp, and RelativeHumidity at 925, 850, 700, 500, and 300 hPa, as well as CIN, CAPE, if not specified.

    Inputs:
    - wrfout_dir: Directory containing WRF output files.
    - output_dir: Directory where the CSV file will be saved.
    - variable_names: List of variable names to include in the CSV file (optional).
    - place: Predefined location name (optional -- lat and lon may be provided instead).
    - lat: Latitude for the location (optional -- place may be provided instead).
    - lon: Longitude for the location (optional -- place may be provided instead).
    - file_tag: String to append to the output filename (optional).
    - domain: Domain for the plots (default is "zoom").

    Returns: The name of the output file saved in the output directory.
    """
    if all(v is None for v in [place, lat, lon]):
        raise ValueError(
            "Either 'place' or both 'lat' and 'lon' must be provided to specify the location for the CSV output."
        )

    if variable_names is None:
        csv_data_v = ["AirTemp", "DewpointTemp", "RelativeHumidity"]
        csv_data_p = [925, 850, 700, 500, 300]
        variable_names = ["CIN", "CAPE"] + [
            f"{var}{height}" for var in csv_data_v for height in csv_data_p
        ]

    defined_variables = sv.get_sv_names()
    undefined_variables = [
        var for var in variable_names if var not in defined_variables
    ]
    if undefined_variables:
        raise ValueError(
            f"Variable(s) '{', '.join(undefined_variables)}' are not defined in SensibleVariables."
            f"Options are: {', '.join(defined_variables)}"
        )
    csv_vars = [set_variable(variable_name=var) for var in variable_names]

    svar = set_variable(
        variable_name="SkewT",  # Placeholder SV for CSV output
        place=place,
        lat=lat,
        lon=lon,
    )
    if place is not None:
        svar.outfile = f"CSV_Data_{place}"
    else:
        svar.outfile = f"CSV_Data_{svar.lat},{svar.lon}"

    outfile = svar.outfile + file_tag

    CSV_Data(
        dir_path=wrfout_dir,
        svariables=csv_vars,
        location=svar,
        outfile=outfile,
        outdir=output_dir,
        domain=domain,
    )

    return outfile
