from datetime import datetime      	###############################################

from netCDF4 import Dataset
from Plot2DField import *
import imageio
import subprocess

print(datetime.now())           	###############################################

Files=[]

# Open the NetCDF file
dir_n="/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/"
wrf_fn="wrfout_d01_2015-06-29_00:00:00"
print("Loading ",wrf_fn)
ncfile = Dataset(dir_n+wrf_fn)

# Get number of time slices and plot them
timerange=ncfile.variables['Times'].shape[0]
#timerange=4
for ti in range(timerange):
	of=wrf_fn+"_t_"+str(ti)+".png"
	Files.append(of)
	print("Processing:",ti+1,"/",timerange, end = '\r')
	Plot2DField(ncfile,"slp","Sea level pressure [hPa] - t="+str(ti),ti,of)
print("Processed successfully.")

# Build GIF
with imageio.get_writer('SLP.gif', mode='I') as writer:
    for filename in Files:
        image = imageio.imread(filename)
        writer.append_data(image)
		
# Remove individual frames
subprocess.run(['rm ./*.png'],shell=True)

print(datetime.now())           	###############################################
