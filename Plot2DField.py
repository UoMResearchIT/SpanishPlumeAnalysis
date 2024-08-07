from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LogNorm, BoundaryNorm
import numpy as np
import cartopy.crs as crs
import cartopy.feature as cfeature
from wrf import to_np, smooth2d, get_cartopy, cartopy_xlim, cartopy_ylim, latlon_coords
import SensibleVariables as sv

# from datetime import datetime      ###############################################
# print(datetime.now())              ###############################################


def Plot2DField(
    var,
    svariable,
    windbarbs=0,
    outfname="MyPlot.png",
    overlap=None,
    u=None,
    v=None,
    smooth=1,
    domain="zoom",
    nlevs=10,
    time_tag=1,
    return_fig=0,
    dpi=100,
    save_pdf=0,
):
    # Input check

    # Need to implement input check here!

    # Gets timestamp
    dtime = str(var.Time.values)[0:19]

    # Smooth the variable
    if smooth:
        smooth_var = smooth2d(var, 3, cenweight=4)
    else:
        smooth_var = var
    thismin = np.nanmin((smooth_var.values))
    thismax = np.nanmax((smooth_var.values))
    # print("min=",thismin," max=",thismax)

    # Get the latitude and longitude points
    lats, lons = latlon_coords(var)
    x = to_np(lons)
    y = to_np(lats)

    # Get the cartopy mapping object
    cart_proj = get_cartopy(var)

    # Create a figure
    fig = plt.figure(figsize=(10.88, 8.16), dpi=dpi)

    # Set the GeoAxes to the projection used by WRF
    ax = plt.axes(projection=cart_proj)

    # Download and add the borders and coastlines	####Takes ~2s
    borders = cfeature.BORDERS.with_scale("50m")
    ax.add_feature(borders, linewidth=0.4, edgecolor="black")
    ax.coastlines("50m", linewidth=0.8)

    # Filled contours
    z = to_np(smooth_var)
    match svariable.scale:
        case "linear":
            nticks = svariable.nticks
            nlevs = svariable.nlevs
            levs = np.linspace(svariable.range_min, svariable.range_max, nlevs)
            norm = Normalize(svariable.range_min, svariable.range_max)
            ticklevs = np.linspace(svariable.range_min, svariable.range_max, nticks)
        case "log":
            levs = np.logspace(
                svariable.range_min,
                svariable.range_max,
                num=svariable.nlevs,
                base=svariable.logbase,
            )
            norm = LogNorm(
                svariable.logbase**svariable.range_min,
                svariable.logbase**svariable.range_max,
            )
            z = np.ma.masked_where(z <= 0, z)
            ticklevs = np.logspace(
                svariable.range_min,
                svariable.range_max,
                num=svariable.nlevs,
                base=svariable.logbase,
            )
        case "bounds":
            levs = svariable.bounds
            norm = BoundaryNorm(levs, len(levs))
            if svariable.hide_edge_ticks:
                ticklevs = levs[1:-1]
            else:
                ticklevs = levs
    contour_fills = plt.contourf(
        x,
        y,
        z,
        levels=levs,
        norm=norm,
        transform=crs.PlateCarree(),
        cmap=svariable.colormap,
        alpha=0.8,
        extend="both",
    )
    if svariable.contour_color is not None:
        contour_lines = plt.contour(
            x,
            y,
            z,
            levels=levs,
            colors=svariable.contour_color,
            linewidths=0.4,
            transform=crs.PlateCarree(),
            extend="both",
        )
        if svariable.contour_c_labels:
            plt.clabel(contour_lines, inline=True, fontsize=8, levels=ticklevs)
    # Add a color bar
    col_bar = plt.colorbar(contour_fills, extendfrac=[0.01, 0.01], ticks=ticklevs)
    if svariable.contour_color is not None:
        col_bar.add_lines(contour_lines)
    plt.annotate(
        "v",
        xy=(
            1.11,
            (
                (thismin - svariable.range_min)
                / (svariable.range_max - svariable.range_min)
            )
            + 0.00,
        ),
        xycoords="axes fraction",
        fontsize=10,
    )
    plt.annotate(
        "ʌ",
        xy=(
            1.11,
            (
                (thismax - svariable.range_min)
                / (svariable.range_max - svariable.range_min)
            )
            - 0.015,
        ),
        xycoords="axes fraction",
        fontsize=10,
    )

    # Overlap empty contours
    if overlap is not None:
        z = to_np(overlap)
        min_z = np.nanmin(z)
        max_z = np.nanmax(z)
        gap = svariable.overlap_gap
        # Adjusts to the nearest multiple of overlap_gap
        adjusted_min_z = int(min_z - (min_z % gap))
        adjusted_max_z = int(max_z + (gap - (max_z % gap)) % gap)
        olevs = list(range(adjusted_min_z, adjusted_max_z, gap))
        ov = plt.contour(
            x,
            y,
            z,
            levels=olevs,
            linewidths=0.4,
            cmap=svariable.overlap_cmap,
            transform=crs.PlateCarree(),
        )
        plt.clabel(ov, inline=True, fontsize=10, levels=olevs[0::2])

    if windbarbs:
        # Convert u and v components to knots
        u = to_np(u)
        v = to_np(v)
        u = u * 1.94384
        v = v * 1.94384
        # Add wind barbs, only plotting every nbarbs
        nbarbs = 25
        ax.barbs(
            x[::nbarbs, ::nbarbs],
            y[::nbarbs, ::nbarbs],
            u[::nbarbs, ::nbarbs],
            v[::nbarbs, ::nbarbs],
            transform=crs.PlateCarree(),
            length=7,
            linewidth=1.0,
        )

    # Set the map bounds
    if domain == "full":
        ax.set_xlim(cartopy_xlim(smooth_var))
        ax.set_ylim(cartopy_ylim(smooth_var))
    elif domain == "UK":
        ax.set_xlim([-1550000, -450000])
        ax.set_ylim([2000000, 3300000])
    else:
        ax.set_xlim([-3542499.4953854363, 942500.950843083])
        ax.set_ylim([-732499.172137629, 3642500.0773183405])

    # Add the gridlines
    ax.gridlines(color="black", linestyle="dotted")

    # Add title and frame time
    plt.title(svariable.ptitle)
    if time_tag:
        plt.annotate(dtime, xy=(0.02, -0.03), xycoords="axes fraction")

    if return_fig:
        return fig
    else:
        plt.savefig(outfname)
        if save_pdf:
            plt.savefig(outfname.replace(".png", ".pdf"))
        plt.close(fig)
