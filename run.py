from Animate import Animate;
import SensibleVariables as sv
from MP4Compare import ConcatNDiff
from WRFCompare import WRFSmoothDiff

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


# ## Generating diagnostics
# dir_path="/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/"
# dout=dir_path.replace('/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/','').replace('run-zrek/','Control').replace('run-zrek.','').replace('/','')
# for wvar in wvarlist:
# 	print("Working on",wvar.outfile)
# 	Animate(dir_path,wvar,
# 		windbarbs=wvar.windbarbs,
# 		outfile=wvar.outfile,
# 		outdir=dout,
# 		smooth=0,
# 		cleanpng=1)

# ## Comparing mp4 files
# d1="Results/Control/"
# d2="Results/Gravity_Waves_fix/"
# cleandiff=1
# l1=d1.replace('Results','').replace('/','')
# l2=d2.replace('Results','').replace('/','')
# dout="vsMP4_"+l1+"-"+l2+"/"
# for wvar in wvarlist:
# 	print("Comparing",wvar.outfile)
# 	ConcatNDiff(wvar.outfile,wvar.outfile,d1,d2,
# 			label1=l1,
# 			label2=l2,
# 			difflabel="| "+l2+" - "+l1+" |",
# 			outfile=wvar.outfile,
# 			outdir=dout,
# 			cleandiff=cleandiff)

## Comparing WRF files
d1="/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/"
d2="/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek.half_hgt/"
l1=d1.replace('/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/','').replace('run-zrek/','Control').replace('run-zrek.','').replace('/','')
l2=d2.replace('/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/','').replace('run-zrek/','Control').replace('run-zrek.','').replace('/','')
dout="vsWRF_"+l1+"-"+l2+"/"
for wvar in wvarlist:
	print("Comparing",wvar.outfile)
	WRFSmoothDiff(d1,d2,wvar,
			windbarbs=wvar.windbarbs,
			smooth=0,
			difflabel="| "+l2+" - "+l1+" |",
			colormap="seismic",
			outfile=wvar.outfile,
			outdir=dout,
			cleanpng=1)

