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
):
    """
    Returns a SensibleVariable with the specified properties.
    """
    try:
        svar = deepcopy(getattr(sv, variable_name))
    except AttributeError:
        raise ValueError(
            f"Variable '{variable_name}' is not defined in SensibleVariables."
            f"Options are: {', '.join(sv.get_sv_names())}"
        )

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
