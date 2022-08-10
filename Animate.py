from netCDF4 import Dataset
from Plot2DField import *
import imageio
import os
from GetSensVar import *

#from datetime import datetime      ###############################################
#print(datetime.now())           	###############################################

#python -c 'from Animate import Animate; Animate("/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/",985,1035,"slp","Sea level pressure [hPa]","slp",1)'
#python -c 'from Animate import Animate; Animate("/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/",270,330,"T2","Temperature at 2m [K]","T2",1)'
#python -c 'from Animate import Animate; Animate("/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/",-20,35,"td2","Dewpoint Temperature at 2m [C?]","td2",1)'

def Animate(dir_path,svariable,windbarbs=0,outfile="MyMP4",outdir="./",smooth=1,cleanpng=1):
	##Input check
    #Directories
    if dir_path[-1]!="/":dir_path=dir_path+"/"
    if outdir[-1]!="/":outdir=outdir+"/"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
	#Need to implement input check here!
    
    #
    print("Generating diagnostic for",svariable.outfile)
    print("Source wrfout files:",dir_path)
    print("Using:\n\twindbarbs=",windbarbs,
                "\n\tsmooth=",smooth,
                "\n\tcleanpng=",cleanpng)
    print("Output will be saved as ",outdir+outfile,"\n")
    
    # Initialization
    WRFfiles=[]
    PNGfiles=[]
    vpv=None
    tmp_dir=outdir+"__"+outfile
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    tmp_dir=tmp_dir+"/"

    # Get list of files from directoy
    for file in os.listdir(dir_path):
        if file.startswith('wrfout'):
            WRFfiles.append(file)
    WRFfiles.sort()

    # Plot each time frame in each file
    for wrf_fn in WRFfiles:
        # Open the NetCDF file
        print("Loading ",wrf_fn)
        ncfile = Dataset(dir_path+wrf_fn)

        # Get number of time frames and plot them
        timerange=ncfile.variables['Times'].shape[0]
#        if timerange>1:timerange=1                              ## For tests only
        for ti in range(timerange):
            of=tmp_dir+outfile+wrf_fn+"_t_"+str(ti)+".png"
            PNGfiles.append(of)
            print("Processing:",ti+1,"/",timerange, end = '\r')
            var,u,v,vpv=GetSensVar(ncfile,svariable,windbarbs,ti,vpv)
            Plot2DField(var,svariable,windbarbs,of,u,v,smooth)
        print("Processed successfully.")

    # Build GIF
    #with imageio.get_writer(outfile+".gif", mode='I') as writer:
    #    for filename in PNGfiles:
    #        image = imageio.imread(filename)
    #        writer.append_data(image)
    # Build mp4
    print("Building MP4 from png files...")
    with imageio.get_writer(outdir+outfile+".mp4", mode='I') as writer:
        for filename in PNGfiles:
            image = imageio.imread(filename)
            writer.append_data(image)

    # Remove individual frame files
    if cleanpng:
        print("Deleting png files...")
        for file in PNGfiles:
            os.remove(file)
        os.removedirs(tmp_dir)
        print("All done.")
