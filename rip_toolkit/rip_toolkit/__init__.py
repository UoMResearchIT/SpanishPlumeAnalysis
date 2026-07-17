from importlib.metadata import PackageNotFoundError, version


from .utils import (
    get_model_times,
    diagnostic_groups,
)
from .api import (
    run_rip_container,
    preprocess,
    point_trajectory,
)

__all__ = [
    "get_model_times",
    "diagnostic_groups",
    "preprocess",
    "point_trajectory",
    "run_rip_container",
]

try:
    __version__ = version("rip_toolkit")
except PackageNotFoundError:
    __version__ = "dev_local_install"
