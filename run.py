from Animate import Animate;
import SensibleVariables as sv

wvarlist=[sv.RelativeHumidity2m,
		  sv.SeaLevelPressure,
		  sv.AirTemp2m,
		  sv.DewpointTemp2m]
	
dir_path="/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/"
cleanpng=1

for wvar in wvarlist:
	Animate(dir_path,wvar,wvar.outfile,cleanpng)
