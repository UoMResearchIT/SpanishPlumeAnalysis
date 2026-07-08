from importlib.metadata import PackageNotFoundError, version

from .ipywidget import (
    view_wrf_3d,
    view_wrf_2d,
)

__all__ = [
    "view_wrf_3d",
    "view_wrf_2d",
]

try:
    __version__ = version("wrf_widget")
except PackageNotFoundError:
    __version__ = "dev_local_install"
