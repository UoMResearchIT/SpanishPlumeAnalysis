from GetSensVar import *
from Plot2DField import *
import os
from wrf import ll_to_xy, to_np, latlon_coords, getvar
import cartopy.crs as crs
import matplotlib.pyplot as plt


def Terrain(
    dir_path,
    svariable,
    outfile="MyTerrain",
    outdir="./",
    out_format="pdf",
    smooth=1,
    domain="zoom",
):

    ##Input check
    # Directories
    if dir_path[-1] != "/":
        dir_path = dir_path + "/"
    if outdir[-1] != "/":
        outdir = outdir + "/"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    # Check requested format is png or pdf only
    out_format = out_format.replace(".", "")
    if out_format not in ["png", "pdf"]:
        print("Output format must be png or pdf. Using default pdf.")
        out_format = "pdf"
    # Output file
    outfname = outdir + outfile + "." + out_format
    # Need to implement input check here!

    #
    print("Generating diagnostic for", svariable.outfile)
    print("Source wrfout files:", dir_path)
    print("Using:\n\tdomain =", domain, "\n\tsmooth    =", smooth)
    print("Output will be saved as ", outfname, "\n")

    # Get list of files from directoy
    WRFfiles = []
    for file in os.listdir(dir_path):
        if file.startswith("wrfout"):
            WRFfiles.append(file)
    WRFfiles.sort()
    ncfile = Dataset(dir_path + WRFfiles[0])
    var, _, _, _ = GetSensVar(ncfile, svariable)

    fig = Plot2DField(
        var,
        svariable,
        0,
        outfname,
        smooth=smooth,
        domain=domain,
        nlevs=11,
        time_tag=0,
        return_fig=1,
        dpi=300,
    )
    # fig = plt.figure(figsize=(10.88,8.16), dpi=300)

    if svariable.lat is not None:
        fig = TerrainPoint(ncfile, svariable, fig)
    plt.savefig(outfname)
    plt.close(fig)


def TerrainPoint(ncfile, svariable, fig):

    print(f"Adding point to map at:")
    print(f"   lat={svariable.lat}")
    print(f"   lon={svariable.lon}")

    # Load wrf variables
    x_y = ll_to_xy(ncfile, svariable.lat, svariable.lon)
    height = getvar(ncfile, "ter", timeidx=0)
    # Prepare variables for metpy
    h = height[x_y[1], x_y[0]].item()

    lats, lons = latlon_coords(height)
    x = to_np(lons)
    y = to_np(lats)

    # Add point to map
    plt.plot(
        x[x_y.data[1], x_y.data[0]],
        y[x_y.data[1], x_y.data[0]],
        linewidth=2,
        marker="o",
        markersize=8,
        markerfacecolor=(0, 0, 0, 0.4),
        markeredgecolor="k",
        transform=crs.PlateCarree(),
    )  # After xy
    plt.plot(
        svariable.lon,
        svariable.lat,
        color="r",
        linewidth=2,
        marker="x",
        transform=crs.PlateCarree(),
    )  # True
    # Add location label
    plt.annotate(
        f"lat={svariable.lat}, lon={svariable.lon}, alt={round(h,1)} m",
        xy=(0.02, 0.94),
        xycoords="axes fraction",
    )
    plt.annotate(
        f"x={x_y.data[0]}, y={x_y.data[1]}", xy=(0.02, 0.92), xycoords="axes fraction"
    )

    return fig
