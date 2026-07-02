from importlib.metadata import version

from .api import (
    diagnostic,
    terrain,
    csv,
    mp4diff,
)

__all__ = [
    "diagnostic",
    "terrain",
    "csv",
    "mp4diff",
]

__version__ = version("wrf_analysis_toolkit")
