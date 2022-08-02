from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import numpy as np
import cartopy.crs as crs
import cartopy.feature as cfeature
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords,g_uvmet,g_geoht,interplevel)
import SensibleVariables as sv

#from datetime import datetime      ###############################################
#print(datetime.now())           	###############################################

def Plot2DField(ncfile,svariable,time,windbarbs,outfname):
	#Input check

	#Need to implement input check here!
	
	
	# Get the variable								####Takes ~5s
	# For simple 2D +value variables
	if svariable.dim==3:
		var = getvar(ncfile, svariable.wrfname, timeidx=time)
		if windbarbs:
			# Get wind speed components at 10m
			u,v=to_np(getvar(ncfile, "uvmet10", timeidx=time))
		#Special variable acquisition			
		if svariable==sv.CAPE:
			var=var[0]
		elif svariable==sv.CIN:
			var=var[1]
	# For 3D +value variables, interpolated at interpvalue of interpvar
	elif svariable.dim==4:
		interpvar = getvar(ncfile,svariable.interpvar,timeidx=time)
		if svariable.wrfname is not None:
			d4var = getvar(ncfile, svariable.wrfname, timeidx=time)
		elif svariable==sv.GeoPotHeight500:
			d4var=g_geoht.get_height(ncfile, timeidx=time)
		var = interplevel(d4var, interpvar, svariable.interpvalue)
		if windbarbs:
			#Get wind speed components at interpvalue
			ua = getvar(ncfile, "ua", timeidx=time)
			va = getvar(ncfile, "va", timeidx=time)
			u=to_np(interplevel(ua, interpvar, svariable.interpvalue))
			v=to_np(interplevel(va, interpvar, svariable.interpvalue))
	#Gets timestamp
	dtime=str(var.Time.values)[0:19]
	
	# Smooth the variable
	smooth_var = smooth2d(var, 3, cenweight=4)
	thismin=np.nanmin((smooth_var.values))
	thismax=np.nanmax((smooth_var.values))
	#print("min=",thismin," max=",thismax)
	
	# Get the latitude and longitude points
	lats, lons = latlon_coords(var)
	x=to_np(lons)
	y=to_np(lats)
	
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
	plt.contourf(x, y, to_np(smooth_var), levels=levs,
				 transform=crs.PlateCarree(),
				 cmap=get_cmap("jet"),alpha=0.8)
	
	# Add a color bar
	plt.colorbar(ax=ax, shrink=.98,ticks=levs[::4])
	plt.annotate("v", xy=(1.11, ((thismin-svariable.range_min)/(svariable.range_max-svariable.range_min))+.01),  xycoords='axes fraction', fontsize=6)
	plt.annotate("ʌ", xy=(1.11, ((thismax-svariable.range_min)/(svariable.range_max-svariable.range_min))-.03),  xycoords='axes fraction', fontsize=6)

	if windbarbs:
		# Add wind barbs, only plotting every nbarbs
		nbarbs=20
		ax.barbs(x[::nbarbs,::nbarbs], y[::nbarbs,::nbarbs],
		u[::nbarbs, ::nbarbs],v[::nbarbs, ::nbarbs], 
		transform=crs.PlateCarree(), length=4,linewidth=0.3)

	# Set the map bounds
	ax.set_xlim(cartopy_xlim(smooth_var))
	ax.set_ylim(cartopy_ylim(smooth_var))

	# Add the gridlines
	ax.gridlines(color="black", linestyle="dotted")

	# Add title and frame time
	plt.title(svariable.ptitle)
	plt.annotate(dtime, xy=(.02, .02),  xycoords='axes fraction')
	
	plt.savefig(outfname)
