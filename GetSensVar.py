from wrf import (to_np, getvar,g_geoht,interplevel)
import SensibleVariables as sv

def GetSensVar(ncfile,svariable,windbarbs=0,time=0):
	u=v=None
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
		#Special variable computation
		if svariable==sv.Rain:
			#Converts Accumulated rain to "instantaneous" rain
			if time>0: tprev=time-1
			else: tprev=0
			varprev=getvar(ncfile, svariable.wrfname, timeidx=tprev)
			var.values=var.values-varprev.values

	# For 3D +value variables, interpolated at interpvalue of interpvar
	elif svariable.dim==4:
		interpvar = getvar(ncfile,svariable.interpvar,timeidx=time)
		if svariable.wrfname is not None:
			d4var = getvar(ncfile, svariable.wrfname, timeidx=time)
		#Special variable acquisition
		elif svariable==sv.GeoPotHeight500:
			d4var=g_geoht.get_height(ncfile, timeidx=time)
		var = interplevel(d4var, interpvar, svariable.interpvalue)
		#Special variable computation
		if svariable==sv.StaticStability700500:
			#Static stability computed as air temperature difference
			var2=interplevel(d4var, interpvar, 500)
			var.values=var.values-var2.values
		if svariable==sv.StaticStability850700:
			#Static stability computed as air temperature difference
			var2=interplevel(d4var, interpvar, 850)
			var.values=var2.values-var.values	
		if windbarbs:
			#Get wind speed components at interpvalue
			ua = getvar(ncfile, "ua", timeidx=time)
			va = getvar(ncfile, "va", timeidx=time)
			u=to_np(interplevel(ua, interpvar, svariable.interpvalue))
			v=to_np(interplevel(va, interpvar, svariable.interpvalue))

	return var,u,v