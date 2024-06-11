from netCDF4 import Dataset
from Plot2DField import *
from SkewT import *
import imageio
import os
from GetSensVar import *
import SensibleVariables as sv

# from datetime import datetime      ###############################################
# print(datetime.now())              ###############################################

# python -c 'from Animate import Animate; Animate("/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/",985,1035,"slp","Sea level pressure [hPa]","slp",1)'
# python -c 'from Animate import Animate; Animate("/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/",270,330,"T2","Temperature at 2m [K]","T2",1)'
# python -c 'from Animate import Animate; Animate("/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/",-20,35,"td2","Dewpoint Temperature at 2m [C?]","td2",1)'


def Animate(
    dir_path,
    svariable,
    windbarbs=0,
    outfile="MyMP4",
    outdir="./",
    smooth=1,
    domain="zoom",
    cleanpng=1,
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

    #
    print("Generating diagnostic for", svariable.outfile)
    print("Source wrfout files:", dir_path)
    print(
        "Using:\n\twindbarbs =",
        windbarbs,
        "\n\tsmooth    =",
        smooth,
        "\n\tcleanpng  =",
        cleanpng,
    )
    print("Output will be saved as ", outdir + outfile, "\n")

    # Initialization
    WRFfiles = []
    PNGfiles = []
    vpv = None
    overlapsv = None
    overlap = None
    tmp_dir = outdir + "__" + outfile
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    tmp_dir = tmp_dir + "/"

    # Get list of files from directoy
    for file in os.listdir(dir_path):
        if file.startswith("wrfout"):
            WRFfiles.append(file)
    WRFfiles.sort()

    if svariable.along_traj:
        # Load trajectory CSV file
        with open(svariable.along_traj, "r") as f:
            print(f"Loading {svariable.along_traj}")
            lines = f.readlines()
            assert lines[0].startswith(
                "Time [h],Latitude [deg],Longitude [deg],Elevation [m],Pressure [mb],"
            ), "Invalid CSV format"
            lines = lines[1:]
            trajectory = [
                {"t": float(t), "lat": float(lat), "lon": float(lon), "p": float(p)}
                for t, lat, lon, z, p, *_ in (x.split(",") for x in lines)
            ]

    # Plot each time frame in each file
    sim_ti = 0
    traj_ti = 0
    for wrf_fn in WRFfiles:
        # Open the NetCDF file
        print("Loading ", wrf_fn)
        ncfile = Dataset(dir_path + wrf_fn)

        # Get number of time frames and plot them
        timerange = ncfile.variables["Times"].shape[0]
        #        if timerange>1:timerange=1                              ## For tests only
        for ti in range(timerange):
            print("Processing:", ti + 1, "/", timerange, end="\r")
            if "SkewT" in svariable.outfile:
                outfname = tmp_dir + outfile + wrf_fn + "_t_" + str(ti) + ".png"
                skip = 0
                if svariable.along_traj:

                    if sim_ti >= trajectory[0]["t"] and sim_ti <= trajectory[-1]["t"]:
                        assert sim_ti == trajectory[traj_ti]["t"], "Invalid time index"
                        svariable.lat = trajectory[traj_ti]["lat"]
                        svariable.lon = trajectory[traj_ti]["lon"]
                        svariable.interpvalue = trajectory[traj_ti]["p"]
                        svariable.ptitle = (
                            f"SkewT along trajectory  ({svariable.lat},{svariable.lon})"
                        )
                        traj_ti += 1
                    else:
                        skip = 1
                if not skip:
                    Plot_SkewT(
                        ncfile,
                        ti,
                        svariable,
                        outfname,
                        save_pdf=save_pdf,
                    )
                    PNGfiles.append(outfname)
                sim_ti = sim_ti + 1
            else:
                var, u, v, vpv = GetSensVar(ncfile, svariable, windbarbs, ti, vpv)
                if svariable.overlap_sv is not None:
                    overlapsv = eval("sv." + svariable.overlap_sv)
                    overlap, _, _, _ = GetSensVar(ncfile, overlapsv, 0, ti, None)
                if var is not None:
                    outfname = tmp_dir + outfile + wrf_fn + "_t_" + str(ti) + ".png"
                    Plot2DField(
                        var,
                        svariable,
                        windbarbs,
                        outfname,
                        overlap,
                        u,
                        v,
                        smooth,
                        domain=domain,
                        save_pdf=save_pdf,
                    )
                    PNGfiles.append(outfname)
        print("Processed successfully.")

    # Build GIF
    # with imageio.get_writer(outfile+".gif", mode='I') as writer:
    #    for filename in PNGfiles:
    #        image = imageio.imread(filename)
    #        writer.append_data(image)
    # Build mp4
    print("Building MP4 from png files...")
    with imageio.get_writer(outdir + outfile + ".mp4", mode="I") as writer:
        for filename in PNGfiles:
            image = imageio.imread(filename)
            writer.append_data(image)

    # Remove individual frame files
    if cleanpng:
        print("Deleting png files...")
        for file in PNGfiles:
            os.remove(file)
        if not save_pdf:
            os.removedirs(tmp_dir)
        print("All done.")
