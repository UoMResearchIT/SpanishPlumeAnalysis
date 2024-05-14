from netCDF4 import Dataset
from wrf import ll_to_xy
import os
import csv
from GetSensVar import *
import SensibleVariables as sv


def CSV_Data(
    dir_path,
    svariables,
    location,
    outfile="MyCSV",
    outdir="./",
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
    # Need to implement input check here!

    #
    print("Generating CSV data file for", outfile)
    print("Variables to extract:")
    for svariable in svariables:
        print("    - ", svariable.outfile)
    print("Source wrfout files:", dir_path)
    print("Using:\n\tdomain =", domain)
    print("Output will be saved as ", outdir + outfile, "\n")

    # Initialization
    WRFfiles = []
    tmp_dir = outdir + "__" + outfile
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    tmp_dir = tmp_dir + "/"

    # Get list of files from directoy
    for file in os.listdir(dir_path):
        if file.startswith("wrfout"):
            WRFfiles.append(file)
    WRFfiles.sort()

    ################## Continue editing here!!!!

    with open(tmp_dir + outfile + ".csv", "w", newline="") as f:
        # Write header
        writer = csv.writer(f)
        writer.writerow(["Timestamp"] + [svariable.outfile for svariable in svariables])

        # Get data from each time frame in each file
        for wrf_fn in WRFfiles:
            # Open the NetCDF file
            print("Loading ", wrf_fn)
            ncfile = Dataset(dir_path + wrf_fn)

            # Get location in x,y coordinates
            x_y = ll_to_xy(ncfile, location.lat, location.lon)
            lat = x_y[0]
            lon = x_y[1]
            # print("Original:", location.lat, location.lon)
            # print("Location:", lat, lon)

            # Get number of time frames and plot them
            timerange = ncfile.variables["Times"].shape[0]
            for ti in range(timerange):
                print("Processing:", ti + 1, "/", timerange, end="\r")
                row = {}
                for svariable in svariables:
                    var, u, v, vpv = GetSensVar(ncfile, svariable, 0, ti, None)
                    if var is not None:
                        # Get value at location
                        value = var.sel(south_north=lat, west_east=lon)
                        row[svariable.outfile] = value.values
                    else:
                        row[svariable.outfile] = None
                writer.writerow(
                    [str(var.Time.values)[0:19]]
                    + [row[svariable.outfile] for svariable in svariables]
                )

            # Close the NetCDF file
            ncfile.close()
            print("Processed successfully.")

    # Move file to output directory
    os.rename(tmp_dir + outfile + ".csv", outdir + outfile + ".csv")
    os.removedirs(tmp_dir)
    print("All done.")
