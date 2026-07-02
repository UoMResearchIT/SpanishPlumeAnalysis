from importlib.metadata import version

from numpy import diff

from .api import (
    diagnostic,
    terrain,
    csv,
    wrfdiff,
    mp4diff,
)

__all__ = [
    "diagnostic",
    "terrain",
    "csv",
    "wrfdiff",
    "mp4diff",
]

__version__ = version("wrf_analysis_toolkit")
