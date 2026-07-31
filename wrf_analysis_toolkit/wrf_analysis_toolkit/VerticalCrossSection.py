from netCDF4 import Dataset
import os
from wrf import to_np, getvar, CoordPair, vertcross

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
    smooth=1,
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

    # Organise files to analyse
    print("Generating vertical cross-section for", svariable.outfile)
    print(f"From ({start_latlon}) to ({end_latlon})")
    WRFfiles = select_wrfout_files(dir_path, time_from, time_to)
    print("Source wrfout files:", dir_path)
    for f in WRFfiles:
        print("  ", f)
    print(
        "\n\tsmooth    =",
        smooth,
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

    # Plot each time frame in each file
    for wrf_fn in WRFfiles:
        # Open the NetCDF file
        print("Loading ", wrf_fn)
        ncfile = Dataset(dir_path + wrf_fn)

        # Get number of time frames and plot them
        timerange = ncfile.variables["Times"].shape[0]
        for ti in range(timerange):
            print("Processing:", ti + 1, "/", timerange, end="\r")
