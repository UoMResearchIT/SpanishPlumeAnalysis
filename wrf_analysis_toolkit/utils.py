import os
from copy import deepcopy

import wrf_analysis_toolkit.SensibleVariables as sv


def str2bool(s):
    if isinstance(s, bool):
        return s
    if s.lower() in ("yes", "true", "t", "y", "1"):
        return 1
    elif s.lower() in ("no", "false", "f", "n", "0"):
        return 0
    else:
        raise Exception("Boolean value expected.")


def set_variable(
    variable_name: str,
    range_min=None,
    range_max=None,
    windbarbs=None,
    place=None,
    lat=None,
    lon=None,
    trajectory=None,
    sens_var=None,
):
    """
    Returns a SensibleVariable with the specified properties.
    """
    if sens_var is None:
        try:
            svar = deepcopy(getattr(sv, variable_name))
        except AttributeError:
            raise ValueError(
                f"Variable '{variable_name}' is not defined in SensibleVariables."
                f"Options are: {', '.join(sv.get_sv_names())}"
            )
    else:
        svar = deepcopy(sens_var)

    if range_min is not None:
        svar.range_min = float(range_min)
    if range_max is not None:
        svar.range_max = float(range_max)

    if windbarbs is not None:
        svar.windbarbs = str2bool(windbarbs)

    if place is not None:
        try:
            point = getattr(sv, f"SkewT_{place}")
        except AttributeError:
            raise ValueError(
                f"Place '{place}' is not defined in SensibleVariables."
                f"Options are: {', '.join(sv.get_sv_places())}"
            )
        svar.lat = point.lat
        svar.lon = point.lon

    if (lat is not None and lon is None) or (lat is None and lon is not None):
        raise ValueError("Both 'lat' and 'lon' must be provided together.")
    if lat is not None:
        svar.lat = float(lat)
    if lon is not None:
        svar.lon = float(lon)

    if trajectory is not None:
        svar.along_traj = trajectory
        trajname = os.path.splitext(os.path.basename(trajectory))[0]
        svar.outfile = f"SkewT_Traj_{trajname}"

    if "SkewT" in svar.outfile and (lat is not None or lon is not None):
        svar.outfile = f"SkewT_at_{svar.lat}_{svar.lon}"
        svar.ptitle = f"SkewT at {svar.lat},{svar.lon}"

    return svar


def check_timestamp(timestamp: str):
    """
    Checks if the timestamp is in the format YYYY-MM-DD_HH:MM:SS.
    Raises a ValueError if the format is invalid.
    """
    import re

    pattern = r"^\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}$"
    if not re.match(pattern, timestamp):
        raise ValueError(
            f"Invalid timestamp format: {timestamp}. Expected format is YYYY-MM-DD_HH:MM:SS."
        )
    return timestamp


def select_wrfout_files(wrfout_dir: str, time_from: str = None, time_to: str = None):
    """
    Returns a list of WRF output files in the specified directory, optionally filtered by time range.
    Expect the files to be named in the format "wrfout_*_YYYY-MM-DD_HH:MM:SS", where * is a wildcard.

    By default, all files starting with "wrfout_" are included.

    If time_from is provided, only files with timestamps >= time_from are included.
    If time_to is provided, only files with timestamps <= time_to are included.
    """
    WRFfiles = sorted(f for f in os.listdir(wrfout_dir) if f.startswith("wrfout_"))

    if time_from is not None:
        check_timestamp(time_from)
        WRFfiles = [f for f in WRFfiles if check_timestamp(f[-19:]) >= time_from]
    if time_to is not None:
        check_timestamp(time_to)
        WRFfiles = [f for f in WRFfiles if check_timestamp(f[-19:]) <= time_to]

    return WRFfiles
