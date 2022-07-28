from netCDF4 import Dataset
from Plot2DField import *
import imageio
import os
#from datetime import datetime      ###############################################
#print(datetime.now())           	###############################################

#python -c 'from Animate import Animate; Animate("/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/",985,1035,"slp","Sea level pressure [hPa]","slp",1)'
#python -c 'from Animate import Animate; Animate("/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/",270,330,"T2","Temperature at 2m [K]","T2",1)'
#python -c 'from Animate import Animate; Animate("/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/",-20,40,"td2","Dewpoint Temperature at 2m [C?]","td2",1)'

def Animate(dir_path,range_min,range_max,variable,ptitle,outfile,cleanpng):
    
	#Input check

	#Need to implement input check here!
    
    # Initialization
    WRFfiles=[]
    PNGfiles=[]

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
            of=outfile+wrf_fn+"_t_"+str(ti)+".png"
            PNGfiles.append(of)
            print("Processing:",ti+1,"/",timerange, end = '\r')
            Plot2DField(ncfile,variable,ptitle,range_min,range_max,ti,of)
        print("Processed successfully.")

    # Build GIF
    #with imageio.get_writer(outfile+".gif", mode='I') as writer:
    #    for filename in PNGfiles:
    #        image = imageio.imread(filename)
    #        writer.append_data(image)
    # Build mp4
    with imageio.get_writer(outfile+".mp4", mode='I') as writer:
        for filename in PNGfiles:
            image = imageio.imread(filename)
            writer.append_data(image)

    # Remove individual frame files
    if cleanpng:
        for file in PNGfiles:
            os.remove(file)
