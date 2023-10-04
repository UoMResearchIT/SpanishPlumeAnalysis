from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.colors import (Normalize, LogNorm, BoundaryNorm)
import numpy as np
import cartopy.crs as crs
import cartopy.feature as cfeature
from wrf import (to_np, smooth2d, get_cartopy, cartopy_xlim,cartopy_ylim, latlon_coords)
import SensibleVariables as sv

#from datetime import datetime      ###############################################
#print(datetime.now())           	###############################################

def Plot2DField(var,svariable,windbarbs=0,outfname="MyPlot.png",overlap=None,u=None,v=None,smooth=1,domain="zoom",nlevs=10):
	#Input check

	#Need to implement input check here!
		
	#Gets timestamp
	dtime=str(var.Time.values)[0:19]
	
	# Smooth the variable
	if smooth:
		smooth_var = smooth2d(var, 3, cenweight=4)
	else:
		smooth_var=var
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
	fig.set_size_inches(10.88,8.16)
	fig.set_dpi(100)
	
	# Set the GeoAxes to the projection used by WRF
	ax = plt.axes(projection=cart_proj)
	
	# Download and add the borders and coastlines	####Takes ~2s
	borders = cfeature.BORDERS.with_scale('50m')
	ax.add_feature(borders, linewidth=.4, edgecolor="black")
	ax.coastlines('50m', linewidth=0.8)

	# Filled contours
	z = to_np(smooth_var)
	match svariable.scale:
		case "linear":
			levs = np.linspace(svariable.range_min, svariable.range_max, nlevs)
			norm = Normalize(svariable.range_min,svariable.range_max)
			ticklevs = np.linspace(svariable.range_min, svariable.range_max, 5)
		case "log":
			levs = np.logspace(svariable.range_min, svariable.range_max, num=svariable.numloglevs, base=svariable.logbase)
			norm = LogNorm(svariable.logbase**svariable.range_min,svariable.logbase**svariable.range_max)
			z = np.ma.masked_where(z <= 0, z)
			ticklevs = np.logspace(svariable.range_min, svariable.range_max, num=svariable.numloglevs, base=svariable.logbase)
		case "bounds":
			levs = svariable.bounds
			norm = BoundaryNorm(levs,len(levs))
			ticklevs = levs[1:-1]
	plt.contourf(x, y, z,
				 levels=levs, norm=norm,
				 transform=crs.PlateCarree(),
				 cmap=svariable.colormap,alpha=0.8,
				 extend="both")
	# Add a color bar
	plt.colorbar(ax=ax, extendfrac=[0.01,0.01],ticks=ticklevs)
	plt.annotate("v", xy=(1.11, ((thismin-svariable.range_min)/(svariable.range_max-svariable.range_min))+.00),  xycoords='axes fraction', fontsize=10)
	plt.annotate("ʌ", xy=(1.11, ((thismax-svariable.range_min)/(svariable.range_max-svariable.range_min))-.015),  xycoords='axes fraction', fontsize=10)

	# Overlap empty contours
	if overlap is not None:
		z = to_np(overlap)
		olevs=list(range(int(np.nanmin(z)), int(np.nanmax(z)),svariable.overlap_gap))
		ov=plt.contour(x, y, z,
				levels=olevs,
				inewidths=0.4, cmap=svariable.overlap_cmap,
				transform=crs.PlateCarree())
		plt.clabel(ov,inline=True, fontsize=10,levels=olevs[0::2])

	if windbarbs:
		# Add wind barbs, only plotting every nbarbs
		nbarbs=20
		ax.barbs(x[::nbarbs,::nbarbs], y[::nbarbs,::nbarbs],
		u[::nbarbs, ::nbarbs],v[::nbarbs, ::nbarbs], 
		transform=crs.PlateCarree(), length=4,linewidth=0.3)

	# Set the map bounds
	if domain=="full":
		ax.set_xlim(cartopy_xlim(smooth_var))
		ax.set_ylim(cartopy_ylim(smooth_var))
	else:
		ax.set_xlim([-3542499.4953854363, 942500.950843083])
		ax.set_ylim([-732499.172137629, 3642500.0773183405])

	# Add the gridlines
	ax.gridlines(color="black", linestyle="dotted")

	# Add title and frame time
	plt.title(svariable.ptitle)
	plt.annotate(dtime, xy=(.02, .02),  xycoords='axes fraction')
	
	plt.savefig(outfname)
