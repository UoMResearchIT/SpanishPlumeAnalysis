from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import numpy as np
import cartopy.crs as crs
import cartopy.feature as cfeature
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords,extract_times,interplevel)

#from datetime import datetime      ###############################################
#print(datetime.now())           	###############################################

def Plot2DField(ncfile,svariable,time,outfname):
	#Input check

	#Need to implement input check here!
	
	
	# Get the variable								####Takes ~5s
	# For simple 2D +value variables
	if svariable.dim==3:
		var = getvar(ncfile, svariable.wrfname, timeidx=time)
	# For 3D +value variables, interpolated at interpvalue of interpvar
	elif svariable.dim==4:
		interpvar=p = getvar(ncfile,svariable.interpvar,timeidx=time)
		d4var = getvar(ncfile, svariable.wrfname, timeidx=time)
		var = interplevel(d4var, interpvar, svariable.interpvalue)
	#Gets timestamp
	dtime=str(var.Time.values)[0:19]
	
	# Smooth the variable
	smooth_var = smooth2d(var, 3, cenweight=4)
	thismin=np.nanmin((smooth_var.values))
	thismax=np.nanmax((smooth_var.values))
	
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

	# Filled contours
	levs = np.linspace(svariable.range_min, svariable.range_max, 21)
	plt.contourf(to_np(lons), to_np(lats), to_np(smooth_var), levels=levs,
				 transform=crs.PlateCarree(),
				 cmap=get_cmap("jet"),alpha=0.8)
	
	# Add a color bar
	plt.colorbar(ax=ax, shrink=.98,ticks=levs[::4])
	plt.annotate("v", xy=(1.11, ((thismin-svariable.range_min)/(svariable.range_max-svariable.range_min))-.05),  xycoords='axes fraction', fontsize=6)
	plt.annotate("ʌ", xy=(1.11, ((thismax-svariable.range_min)/(svariable.range_max-svariable.range_min))-.03),  xycoords='axes fraction', fontsize=6)

	# Set the map bounds
	ax.set_xlim(cartopy_xlim(smooth_var))
	ax.set_ylim(cartopy_ylim(smooth_var))

	# Add the gridlines
	ax.gridlines(color="black", linestyle="dotted")

	# Add title and frame time
	plt.title(svariable.ptitle)
	plt.annotate(dtime, xy=(.02, .02),  xycoords='axes fraction')
	
	plt.savefig(outfname)
