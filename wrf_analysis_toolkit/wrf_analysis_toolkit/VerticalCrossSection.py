from netCDF4 import Dataset
import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import get_cmap
from matplotlib.ticker import ScalarFormatter

from wrf import to_np, getvar, CoordPair, vertcross, ll_to_xy

from wrf_analysis_toolkit.utils import select_wrfout_files
from wrf_analysis_toolkit.GetSensVar import *
import wrf_analysis_toolkit.SensibleVariables as sv

def VerticalCrossSection(
    dir_path,
    svariable,
    start_latlon,
    end_latlon,
    time_from=None,
    time_to=None,
    outfile="VertCrossSec",
    outdir="./",
    time_tag=1,
    dpi=100,
    cleanpng=0,
    save_pdf=0,
):
    ##Input check
    # Directories
    if dir_path[-1] != "/":
        dir_path = dir_path + "/"
    if outdir[-1] != "/":
        outdir = outdir + "/"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    # Need to implement input check here!

    if start_latlon is None or start_latlon is None:
        raise ValueError("start_latlon and end_latlon must be defined to make a vertical cross-section")

    start_point = CoordPair(lat=start_latlon[0], lon=start_latlon[1])
    end_point = CoordPair(lat=end_latlon[0], lon=end_latlon[1])

    # Organise files to analyse
    print(f"Generating vertical cross-section for {svariable.outfile}")
    print(f"From {start_point.latlon_str} to {end_point.latlon_str}")
    WRFfiles = select_wrfout_files(dir_path, time_from, time_to)
    print("Source wrfout files:", dir_path)
    for f in WRFfiles:
        print("  ", f)
    print(
        "\n\tcleanpng  =",
        cleanpng,
    )
    print("Output will be saved as ", outdir + outfile, "\n")

    # Initialization
    PNGfiles = []
    tmp_dir = outdir + "__" + outfile
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    tmp_dir = tmp_dir + "/"

    levs = np.linspace(svariable.range_min, svariable.range_max, svariable.nlevs)
    ticklevs = np.linspace(svariable.range_min, svariable.range_max, svariable.nlevs)

    # Plot each time frame in each file
    latlon_passed = False
    for wrf_fn in WRFfiles:
        # Open the NetCDF file
        print("Loading ", wrf_fn)
        ncfile = Dataset(dir_path + wrf_fn)

        # Confirm start/end latpoints are inside the domain
        if not latlon_passed:
            latlon_check(ncfile, start_point)
            latlon_check(ncfile, end_point)
            latlon_passed = True

        # Get number of time frames and plot them
        timerange = ncfile.variables["Times"].shape[0]
        for ti in range(timerange):
            print("Processing:", ti + 1, "/", timerange, end="\r")
            outfname = tmp_dir + outfile + wrf_fn + "_t_" + str(ti) + ".png"

            # Extract variable along pressure coordinates
            var =  getvar(ncfile, svariable.wrfname)
            dtime = str(var.Time.values)[0:19]
            p = getvar(ncfile, "pressure")
            var_cross = vertcross(
                var,
                p,
                wrfin=ncfile,
                start_point=start_point,
                end_point=end_point,
                latlon=True,
                meta=True
            )

            # Create a figure
            fig = plt.figure(figsize=(10.88, 7.16), dpi=dpi)
            ax = plt.axes()
            coord_pairs = to_np(var_cross.coords["xy_loc"])
            var_contours = ax.contourf(
                np.arange(coord_pairs.shape[0]),
                to_np(var_cross["vertical"]), 
                to_np(var_cross),
                levels=levs,
                cmap=get_cmap(svariable.colormap)
            )
            col_bar = plt.colorbar(
                var_contours,
                extendfrac=[0.01, 0.01],
                ticks=ticklevs
            )

            # Arrange x-axis labels - latlon pairs
            x_ticks = np.arange(coord_pairs.shape[0])
            x_labels = [
                pair.latlon_str(fmt="{:.2f}, {:.2f}") for pair in to_np(coord_pairs)
            ]
            ax.set_xticks(x_ticks[::10])
            ax.set_xticklabels(x_labels[::10], rotation=45, fontsize=10)
            ax.set_xlabel("Latitude/Longitude", fontsize=12)

            # Arrange y-axis labels - pressure
            ax.set_yscale('symlog')
            ax.yaxis.set_major_formatter(ScalarFormatter())
            ax.set_yticks(np.linspace(100, 1000, 10))
            ax.set_ylim(1000, 100)
            ax.set_ylabel("Pressure (hPa)", fontsize=12)

            plt.title(f"{svariable.ptitle} at {dtime}")

            plt.savefig(outfname)
            if save_pdf:
                plt.savefig(outfname.replace(".png", ".pdf"))
            plt.close(fig)


def latlon_check(ncfile: Dataset, coord_pair: CoordPair):
    lat = coord_pair.lat
    lon = coord_pair.lon
    try:
        x_y = ll_to_xy(ncfile, lat, lon)
    except ValueError as err:
        raise ValueError(
            f"Point ({lat}, {lon}) is outside the WRF domain"
        ) from err
