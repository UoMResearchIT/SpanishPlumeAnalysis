import metpy as mp
from metpy.units import units
from metpy.plots import SkewT
from wrf import (ll_to_xy, getvar, get_cartopy, xy_to_ll, to_np, latlon_coords)
import cartopy.feature as cfeature
import cartopy.crs as crs
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import numpy as np
import SensibleVariables as sv

def Plot_SkewT(ncfile,ti,svariable,outfname="MyPlot.png"):

    # Load wrf variables
    x_y = ll_to_xy(ncfile,svariable.lat, svariable.lon)
    height = getvar(ncfile,"ter",timeidx=ti)
    p1  = getvar(ncfile,"pressure",timeidx=ti)
    T1  = getvar(ncfile,"tc",timeidx=ti)
    Td1 = getvar(ncfile,"td",timeidx=ti)
    u1  = getvar(ncfile,"ua",timeidx=ti)
    v1  = getvar(ncfile,"va",timeidx=ti)
    # Extract date time for label
    dtime=str(p1.Time.values)[0:19]
    # Prepare variables for metpy
    h = height[x_y[0],x_y[1]].data  * units.m
    p  = p1[:,x_y[0],x_y[1]].data  * units.hPa 
    T  = T1[:,x_y[0],x_y[1]].data  * units.degC
    Td = Td1[:,x_y[0],x_y[1]].data * units.degC
    u  = v1[:,x_y[0],x_y[1]].data  * units('m/s')
    v  = u1[:,x_y[0],x_y[1]].data  * units('m/s')

    # print(height)
    # print(p)
    print(f"lat,lon={svariable.lat},{svariable.lon}")
    print(f"x_y.data={x_y.data}")
    llll=xy_to_ll(ncfile,x_y[0],x_y[1],timeidx=ti)
    print(f"llll.data={llll.data}")
    print(f"h={h}")
    # Get the cartopy mapping object
    cart_proj = get_cartopy(height)
    # Create a figure
    fig = plt.figure(figsize=(10.88,8.16), dpi=300)
    # Set the GeoAxes to the projection used by WRF
    ax = plt.axes(projection=cart_proj)
    # Download and add the borders and coastlines	####Takes ~2s
    borders = cfeature.BORDERS.with_scale('50m')
    ax.add_feature(borders, linewidth=.4, edgecolor="black")
    ax.coastlines('50m', linewidth=0.8)
    #Terrain filled contours
    lats, lons = latlon_coords(height)
    x=to_np(lons)
    y=to_np(lats)
    z=to_np(height)
    print(f"x={x[x_y.data[0],x_y.data[1]]}")
    print(f"y={y[x_y.data[0],x_y.data[1]]}")
    print(f"z={z[x_y.data[0],x_y.data[1]]}")
    nticks = sv.TerrainElevation.nticks
    nlevs = sv.TerrainElevation.nlevs
    levs = np.linspace(sv.TerrainElevation.range_min, sv.TerrainElevation.range_max, nlevs)
    norm = Normalize(sv.TerrainElevation.range_min,sv.TerrainElevation.range_max)
    ticklevs = np.linspace(sv.TerrainElevation.range_min, sv.TerrainElevation.range_max, nticks)
    plt.contourf(x, y, z,
				 levels=levs, norm=norm,
				 transform=crs.PlateCarree(),
				 cmap=sv.TerrainElevation.colormap,alpha=0.8,
				 extend="both")
    plt.colorbar(ax=ax, extendfrac=[0.01,0.01],ticks=ticklevs)
    # Adds marker to location on map
    plt.plot(float(svariable.lon), float(svariable.lat), color='darkred', linewidth=2, marker='x', transform=crs.PlateCarree())         # True
    plt.plot(llll.data[1], llll.data[0], color='red', linewidth=2, marker='x', transform=crs.PlateCarree())                             # After xy
    plt.plot(x[x_y.data[0],x_y.data[1]], y[x_y.data[0],x_y.data[1]], color='m', linewidth=2, marker='x', transform=crs.PlateCarree())   # Where i think its actually checking
    # Set the map bounds
    ax.set_xlim([-3542499.4953854363, 942500.950843083])
    ax.set_ylim([-732499.172137629, 3642500.0773183405])
    # Add the gridlines
    ax.gridlines(color="black", linestyle="dotted")
    # Add title and frame time
    plt.annotate(f"lat={svariable.lat}, lon={svariable.lon}, alt={round(h.magnitude,1)} m", xy=(.02, .02),  xycoords='axes fraction')
    plt.savefig(f"{outfname}_map.png")
    plt.close(fig)

    # Create figure
    fig = plt.figure(figsize=(10.88,8.16), dpi=100)
    skew = SkewT(fig=fig)
    skew.ax.set_ylim(1000, 100)
    skew.ax.set_xlim(svariable.range_min, svariable.range_max)
    skew.ax.set_xlabel('Temperature [$^\circ$C]')
    skew.ax.set_ylabel('Pressure [hPa]')

    # Shade every other isotherm
    isothermal_values = np.arange(-100,1001,10)
    for i in range(len(isothermal_values) - 1)[::2]:
        skew.ax.fill_betweenx(p, isothermal_values[i], isothermal_values[i+1], color='gray', alpha=0.1)
    # skew.ax.axvline(0, color='c', linestyle='-', linewidth=1.5)         # Zero degree isotherm

    # Plot only some windbarbs
    my_interval = np.arange(100, 1000, 50) * units('mbar')
    ix = mp.calc.resample_nn_1d(p, my_interval)
    skew.plot_barbs(p[ix], u[ix], v[ix])

    # Plot LCL temperature as black dot
    lcl_pressure, lcl_temperature = mp.calc.lcl(p[0], T[0], Td[0])
    skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')
    # Calculate the parcel profile and plot as black line
    parcel_prof = mp.calc.parcel_profile(p, T[0], Td[0]).to('degC')
    skew.plot(p, parcel_prof, 'k', linewidth=2)
    # Adds CAPE and CIN
    skew.shade_cape(p, T, parcel_prof)
    skew.shade_cin(p, T, parcel_prof, Td)
    cape_cin=mp.calc.cape_cin(p, T, Td, parcel_prof)
    plt.annotate(f"CAPE: {round(cape_cin[0].magnitude,1)}", xy=(.84, .97),  xycoords='axes fraction',
                    bbox=dict(boxstyle='round', facecolor='red', alpha=0.3))
    plt.annotate(f"  CIN: {round(cape_cin[1].magnitude,1)}", xy=(.84, .93),  xycoords='axes fraction',
                    bbox=dict(boxstyle='round', facecolor='cornflowerblue', alpha=0.3))

    # Add background lines
    skew.plot_dry_adiabats(color='red', linestyle='-', linewidth=1)     # Dry adiabats (default to red)
    skew.plot_moist_adiabats(color='blue', linestyle='-', linewidth=1)  # Moist adiabats (default to blue)
    skew.plot_mixing_lines(color='green', linestyle='--', linewidth=1)  # Mixing lines (default to green)

    # Plot Temperature and Dew Point Temperature
    skew.plot(p, T, color='red')
    skew.plot(p, Td, color='green')

    # Add title, frame time, save and close
    plt.title(svariable.ptitle)
    plt.annotate(dtime, xy=(.01, .01),  xycoords='figure fraction')
    plt.savefig(outfname)
    plt.close(fig)
