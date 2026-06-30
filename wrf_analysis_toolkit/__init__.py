from importlib.metadata import version

from .api import (
    diagnostic,
    terrain,
)

__all__ = [
    "diagnostic",
    "terrain",
]

__version__ = version("wrf_analysis_toolkit")
