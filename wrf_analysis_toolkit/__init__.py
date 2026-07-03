from importlib.metadata import version

from numpy import diff

from .api import (
    diagnostic,
    terrain,
    csv,
    wrfdiff,
    mp4diff,
    mp4stitch,
)

__all__ = [
    "diagnostic",
    "terrain",
    "csv",
    "wrfdiff",
    "mp4diff",
    "mp4stitch",
]

__version__ = version("wrf_analysis_toolkit")
