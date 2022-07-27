#from datetime import datetime      ###############################################
#print(datetime.now())           	###############################################

from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
#from cartopy.feature import NaturalEarthFeature
import cartopy.feature as cfeature

from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords)

def Plot2DField(fdir,fname,variable,ptitle,time,outfname):
	if variable =="default":
		variable="slp"
		ptitle="Sea Level Pressure (hPa)"
		time=0
		outfname="default_t=0.png"
	#Need to implement input check here!
	
	# Open the NetCDF file							####Takes ~0.2s
	ncfile = Dataset(fdir+fname)
	
	# Get the variable								####Takes ~5s
	var = getvar(ncfile, variable, timeidx=time)
	
	# Smooth the sea level pressure since it tends to be noisy near the mountains
	smooth_var = smooth2d(var, 3, cenweight=4)

	
	# Get the latitude and longitude points
	lats, lons = latlon_coords(var)
	
	# Get the cartopy mapping object
	cart_proj = get_cartopy(var)
	
	# Create a figure								####Takes ~7s first time, but reuses preexisting figure
	fig = plt.gcf()
	plt.clf()
	
	# Set the GeoAxes to the projection used by WRF
	ax = plt.axes(projection=cart_proj)
	
	# Download and add the borders and coastlines	####Takes ~2s
	borders = cfeature.BORDERS.with_scale('50m')
	ax.add_feature(borders, linewidth=.4, edgecolor="black")
	ax.coastlines('50m', linewidth=0.8)

	# Make the contour outlines 
	#plt.contour(to_np(lons), to_np(lats), to_np(smooth_var), 4, colors="black",
	#            transform=crs.PlateCarree(),linewidths=0.2)
	# Filled contours
	plt.contourf(to_np(lons), to_np(lats), to_np(smooth_var), 16,
				 transform=crs.PlateCarree(),
				 cmap=get_cmap("jet"),alpha=0.8)
	
	# Add a color bar
	plt.colorbar(ax=ax, shrink=.98)

	# Set the map bounds
	ax.set_xlim(cartopy_xlim(smooth_var))
	ax.set_ylim(cartopy_ylim(smooth_var))

	# Add the gridlines
	ax.gridlines(color="black", linestyle="dotted")

	plt.title(ptitle)
	
	plt.savefig(outfname)
	#print("Saved",outfname)
	#plt.show()