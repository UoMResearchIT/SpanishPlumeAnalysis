import metpy as mp
from metpy.units import units
from metpy.plots import SkewT
from wrf import (ll_to_xy, getvar)
import matplotlib.pyplot as plt
import numpy as np
import SensibleVariables as sv

def Plot_SkewT(ncfile,ti,svariable,outfname="MyPlot.png"):

    # Load wrf variables
    x_y = ll_to_xy(ncfile, svariable.lat, svariable.lon)
    p1 = getvar(ncfile,"pressure",timeidx=ti)
    T1 = getvar(ncfile,"tc",timeidx=ti)
    Td1 = getvar(ncfile,"td",timeidx=ti)
    u1 = getvar(ncfile,"ua",timeidx=ti)
    v1 = getvar(ncfile,"va",timeidx=ti)
    # Extract date time for label
    dtime=str(p1.Time.values)[0:19]
    # Prepare variables for metpy
    p = units.hPa  * p1[:,x_y[0],x_y[1]]
    T = units.degC * T1[:,x_y[0],x_y[1]]
    Td = units.degC * Td1[:,x_y[0],x_y[1]]
    u = units('m/s') * v1[:,x_y[0],x_y[1]]
    v = units('m/s') * u1[:,x_y[0],x_y[1]]

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
    skew.ax.axvline(0, color='c', linestyle='-', linewidth=1.5)         # Zero degree isotherm

    # Plot only some windbarbs
    my_interval = np.arange(100, 1000, 50) * units('mbar')
    ix = mp.calc.resample_nn_1d(p, my_interval)
    skew.plot_barbs(p[ix], u[ix], v[ix])

    # Plot LCL temperature as black dot
    lcl_pressure, lcl_temperature = mp.calc.lcl(p[0], T[0], Td[0])
    skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')
    # Calculate the parcel profile and plot as black line
    parcel_prof = mp.calc.parcel_profile(p, T[0], Td[0]).metpy.unit_array.to('degC')
    skew.plot(p, parcel_prof, 'k', linewidth=2)
    skew.shade_cin(p.metpy.unit_array.to('hPa'), T.metpy.unit_array.to('degC'), parcel_prof, Td.metpy.unit_array.to('degC'))    # Shaded CIN not sure if its working...
    skew.shade_cape(p.metpy.unit_array.to('hPa'), T.metpy.unit_array.to('degC'), parcel_prof)   # Shaded CAPE not sure if its working...

    # Add background lines
    skew.plot_dry_adiabats(color='red', linestyle='-', linewidth=1)     # Dry adiabats (default to red)
    skew.plot_moist_adiabats(color='blue', linestyle='-', linewidth=1)  # Moist adiabats (default to blue)
    skew.plot_mixing_lines(color='green', linestyle='--', linewidth=1)  # Mixing lines (default to green)

    # Plot Temperature and Dew Point Temperature
    skew.plot(p, T, 'r')
    skew.plot(p, Td, 'g')

    # Add title, frame time, save and close
    plt.title(svariable.ptitle)
    plt.annotate(dtime, xy=(.01, .01),  xycoords='figure fraction')
    plt.savefig(outfname)
    plt.close
