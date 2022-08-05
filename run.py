from Animate import Animate;
import SensibleVariables as sv
from MP4Compare import ConcatNDiff

wvarlist=[sv.SeaLevelPressure,
		  sv.AirTemp2m,
		  sv.DewpointTemp2m,
		  sv.RelativeHumidity2m,
		  sv.CAPE,
		  sv.CIN,
		  sv.Rain,
		  sv.AirTemp850,
		  sv.DewpointTemp850,
		  sv.GeoPotHeight500,
		  sv.StaticStability700500,
		  sv.StaticStability850700]
	

## Generating diagnostics
# dir_path="/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/"
# cleanpng=1
# for wvar in wvarlist:
# 	print("Working on",wvar.outfile)
# 	Animate(dir_path,wvar,wvar.windbarbs,wvar.outfile,cleanpng)

## Comparing mp4 files
d1="Results/Control/"
d2="Results/Gravity_Waves_fix/"
dout="Results/vs_Control-GWavesFix/"
diff=1
for wvar in wvarlist:
	print("Comparing",wvar.outfile)
	ConcatNDiff(wvar.outfile,wvar.outfile,d1,d2,"Control","GWaves_fix",diff,dout+wvar.outfile)