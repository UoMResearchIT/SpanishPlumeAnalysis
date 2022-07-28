from datetime import datetime      	###############################################

from netCDF4 import Dataset
from Plot2DField import *
import imageio
import os

print(datetime.now())           	###############################################


WRFfiles=[]
PNGfiles=[]


dir_path="/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/"

#Get list of files from directoy
for file in os.listdir(dir_path):
    # check only wrfout files
    if file.startswith('wrfout'):
        WRFfiles.append(file)
WRFfiles.sort()

#Plots each time slice in each file
for wrf_fn in WRFfiles:
	# Open the NetCDF file
	print("Loading ",wrf_fn)
	ncfile = Dataset(dir_path+wrf_fn)

	# Get number of time slices and plot them
	timerange=ncfile.variables['Times'].shape[0]
#	if timerange>3:timerange=3
	for ti in range(timerange):
		of=wrf_fn+"_t_"+str(ti)+".png"
		PNGfiles.append(of)
		print("Processing:",ti+1,"/",timerange, end = '\r')
		Plot2DField(ncfile,"slp","Sea level pressure [hPa] - t="+str(ti),ti,of)
	print("Processed successfully.")

# Build GIF
with imageio.get_writer('SLP.gif', mode='I') as writer:
    for filename in PNGfiles:
        image = imageio.imread(filename)
        writer.append_data(image)
		
# Remove individual frames
for file in PNGfiles:
	os.remove(file)

print(datetime.now())           	###############################################
