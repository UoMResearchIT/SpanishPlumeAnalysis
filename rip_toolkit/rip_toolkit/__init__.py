from importlib.metadata import PackageNotFoundError, version

from .api import (
    run_rip_container,
    preprocess,
)
from .utils import (
    get_model_times,
)

__all__ = [
    run_rip_container,
    preprocess,
    get_model_times,
]

try:
    __version__ = version("rip_toolkit")
except PackageNotFoundError:
    __version__ = "dev_local_install"
