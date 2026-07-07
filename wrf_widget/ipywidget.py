import xarray as xr
import matplotlib.pyplot as plt
import ipywidgets as widgets
import numpy as np

def view_wrf_3d(da: xr.DataArray, cmap="viridis"):
    """
    Quick tool for viewing a 3D field from a wrfout file
    """
    if len(da.dims) != 3:
        raise ValueError(f"Input DA must have 3 dimensions, has {len(da.dims)}")

    vmin = np.nanmin(da)
    vmax = np.nanmax(da)
    zdim = da.dims[0]
    @widgets.interact(level=(0, da.sizes[zdim] - 1))
    def view(level=0):
        fig, ax = plt.subplots(figsize=(9, 5))
        im = ax.imshow(
            da.isel({zdim: level}),
            origin="lower",
            cmap=cmap,
            aspect="auto",
            vmin=vmin,
            vmax=vmax
        )
        cbar = plt.colorbar(im, shrink=0.8, aspect=40)
        cbar.set_label(f"{da.name} [{da.units}]")
        plt.title(f"{da.description} Level {level}")
        plt.show()

def view_wrf_2d(da: xr.DataArray, cmap="viridis"):
    """
    Quick tool for viewing a 3D field from a wrfout file
    """
    if len(da.dims) != 2:
        raise ValueError(f"Input DA must have 2 dimensions, has {len(da.dims)}")

    vmin = np.nanmin(da)
    vmax = np.nanmax(da)
    fig, ax = plt.subplots(figsize=(9, 5))
    im = ax.imshow(
        da,
        origin="lower",
        cmap=cmap,
        aspect="auto",
        vmin=vmin,
        vmax=vmax
    )
    cbar = plt.colorbar(im, shrink=0.8, aspect=40)
    cbar.set_label(f"{da.name} [{da.units}]")
    plt.title(f"{da.description}")
    plt.show()
