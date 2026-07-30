from importlib.metadata import PackageNotFoundError, version

from .api import (
    diagnostic,
    terrain,
    csv,
    wrfdiff,
    mp4diff,
    mp4stitch,
    vcross,
)

__all__ = [
    "diagnostic",
    "terrain",
    "csv",
    "wrfdiff",
    "mp4diff",
    "mp4stitch",
    "vcross",
]

try:
    __version__ = version("wrf_analysis_toolkit")
except PackageNotFoundError:
    __version__ = "dev_local_install"
