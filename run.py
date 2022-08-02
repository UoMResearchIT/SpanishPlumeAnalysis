from Animate import Animate;
import SensibleVariables as sv

wvarlist=[sv.SeaLevelPressure,
		  sv.AirTemp2m,
		  sv.DewpointTemp2m
		  sv.RelativeHumidity2m,
		  sv.CAPE,
		  sv.CIN,
		  sv.AirTemp850,
		  sv.DewpointTemp850,
		  sv.GeoPotHeight500]
	
dir_path="/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/"
cleanpng=1

for wvar in wvarlist:
	Animate(dir_path,wvar,wvar.windbarbs,wvar.outfile,cleanpng)
