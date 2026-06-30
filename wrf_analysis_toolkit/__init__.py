from importlib.metadata import version

from .api import (
    diagnostic,
    terrain,
    csv,
)

__all__ = [
    "diagnostic",
    "terrain",
    "csv",
]

__version__ = version("wrf_analysis_toolkit")
