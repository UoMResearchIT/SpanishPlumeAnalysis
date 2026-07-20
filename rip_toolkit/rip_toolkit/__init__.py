from importlib.metadata import PackageNotFoundError, version


from .utils import (
    get_model_times,
    print_model_times,
    diagnostic_groups,
)
from .api import (
    run_rip_container,
    preprocess,
    point_trajectory,
    stack_trajectories,
    plot_trajectories,
)

__all__ = [
    "get_model_times",
    "print_model_times",
    "diagnostic_groups",
    "preprocess",
    "point_trajectory",
    "stack_trajectories",
    "plot_trajectories",
    "run_rip_container",
]

try:
    __version__ = version("rip_toolkit")
except PackageNotFoundError:
    __version__ = "dev_local_install"
