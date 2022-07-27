from datetime import datetime      	###############################################

from Plot2DField import *
import imageio

print(datetime.now())           	###############################################

Files=[]

# NetCDF file
dir_n="/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/"
wrf_fn="wrfout_d01_2015-06-29_00:00:00"
print("Loading ",wrf_fn)

# Loops through time index
trange=4
for ti in range(trange):
	ofile=wrf_fn+"_t_"+str(ti)+".png"
	Files.append(ofile)
	print("Processing:",ti+1,"/",trange, end = '\r')
	Plot2DField(dir_n,wrf_fn,"slp","Sea level pressure [hPa] - t="+str(ti),ti,ofile)
print("Processed successfully.")

# Build GIF
with imageio.get_writer('SLP.gif', mode='I') as writer:
    for filename in Files:
        image = imageio.imread(filename)
        writer.append_data(image)
		
print(datetime.now())           	###############################################