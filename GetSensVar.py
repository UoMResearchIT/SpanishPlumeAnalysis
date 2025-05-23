from wrf import to_np, getvar, g_geoht, interplevel
import SensibleVariables as sv
import Frontogenesis
import numpy as np


def GetSensVar(ncfile, svariable, windbarbs=0, time=0, varprevv=None):
    u = v = varv = None
    # For simple 2D +value variables
    if svariable.dim == 3:
        var = getvar(ncfile, svariable.wrfname, timeidx=time)
        if windbarbs:
            # Get wind speed components at 10m
            u, v = to_np(getvar(ncfile, "uvmet10", timeidx=time))
        # Special variable acquisition
        if svariable == sv.CAPE:
            var = var[0]
        elif (
            svariable == sv.CIN
            or svariable == sv.CIN_YlGnBu
            or svariable == sv.CIN_YlGn
        ):
            var = var[1]
        # Special variable computation
        if svariable == sv.Rain:
            # Adds RAINC and RAINNC to get total accumulated precipitation
            rnc = getvar(ncfile, "RAINNC", timeidx=time)
            var.values = var.values + rnc.values
            # Saves current accumulated total rain to output and use in next time index
            varv = var.values
            # Converts accumulated rain to "hourly" rain (given hourly time indices)
            if varprevv is not None:
                var.values = var.values - varprevv

    # For 3D +value variables, interpolated at interpvalue of interpvar
    elif svariable.dim == 4:
        interpvar = getvar(ncfile, svariable.interpvar, timeidx=time)
        if svariable.wrfname is not None:
            d4var = getvar(ncfile, svariable.wrfname, timeidx=time)
        # Special variable acquisition
        elif svariable.outfile.startswith("GeoPotHeight"):
            d4var = g_geoht.get_height(ncfile, timeidx=time)
        elif "Frontogenesis" in svariable.outfile:
            F3D = Frontogenesis.frontogenesis3D(ncfile, time)
            d4var = getvar(ncfile, svariable.interpvar, timeidx=time)
            d4var.values = F3D
        var = interplevel(d4var, interpvar, svariable.interpvalue)
        # Special variable computation
        if "AirTempDif6h" in svariable.outfile:
            # Temperature difference in 6h
            if varprevv is None:
                varv = [var.values]
                var = None
            else:
                if len(varprevv) < 6:
                    varv = np.append(varprevv, [var.values], axis=0)
                    var = None
                else:
                    varv = np.append(varprevv[1:], [var.values], axis=0)
                    var.values = var.values - varprevv[0]
        elif "AirTempDif12h" in svariable.outfile:
            # Temperature difference in 12h
            if varprevv is None:
                varv = [var.values]
                var = None
            else:
                if len(varprevv) < 12:
                    varv = np.append(varprevv, [var.values], axis=0)
                    var = None
                else:
                    varv = np.append(varprevv[1:], [var.values], axis=0)
                    var.values = var.values - varprevv[0]
        elif svariable == sv.StaticStability700500:
            # Static stability computed as air temperature difference
            var2 = interplevel(d4var, interpvar, 500)
            var.values = var.values - var2.values
        elif svariable == sv.StaticStability850700:
            # Static stability computed as air temperature difference
            var2 = interplevel(d4var, interpvar, 850)
            var.values = var2.values - var.values
        elif svariable == sv.InstRain:
            # InstRain (R) from SimRadarReflectivity1km (dBZ) using Marshall-Palmer: Z = 10^(dBZ/10) = 200*R^1.6
            var.values = (0.005 * 10 ** (0.1 * var.values)) ** (0.625)
        if windbarbs:
            # Get wind speed components at interpvalue
            ua = getvar(ncfile, "ua", timeidx=time)
            va = getvar(ncfile, "va", timeidx=time)
            u = to_np(interplevel(ua, interpvar, svariable.interpvalue))
            v = to_np(interplevel(va, interpvar, svariable.interpvalue))

    return var, u, v, varv
