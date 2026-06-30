import os
from copy import deepcopy

from wrf_analysis_toolkit.utils import set_variable

from wrf_analysis_toolkit.Animate import Animate


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
