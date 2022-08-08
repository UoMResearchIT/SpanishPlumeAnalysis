import sys
#Adds folder to python path search
sys.path.insert(1, '/mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/')
#Gets imputs from csf
task = str(sys.argv[1])
var = str(sys.argv[2])
dir_path = str(sys.argv[3])

from Animate import Animate;
import SensibleVariables as sv
from MP4Compare import ConcatNDiff


match var:
    case "SeaLevelPressure":
        wvar=sv.SeaLevelPressure
    case "AirTemp2m":
        wvar=sv.AirTemp2m
    case "DewpointTemp2m":
        wvar=sv.DewpointTemp2m
    case "RelativeHumidity2m":
        wvar=sv.RelativeHumidity2m
    case "CAPE":
        wvar=sv.CAPE
    case "CIN":
        wvar=sv.CIN
    case "Rain":
        wvar=sv.Rain
    case "AirTemp850":
        wvar=sv.AirTemp850
    case "DewpointTemp850":
        wvar=sv.DewpointTemp850
    case "GeoPotHeight500":
        wvar=sv.GeoPotHeight500
    case "StaticStability700500":
        wvar=sv.StaticStability700500
    case "StaticStability850700":
        wvar=sv.StaticStability850700

match task:
    case "diagnostic":
        # Generating diagnostics
        cleanpng=1
        print("Working on",wvar.outfile)
        Animate(dir_path,wvar,wvar.windbarbs,wvar.outfile,cleanpng)
    case "mp4compare":
        ## Comparing mp4 files
        d1="Results/Control/"
        d2="Results/Gravity_Waves_fix/"
        dout="Results/vs_Control-GWavesFix/"
        diff=1
        print("Comparing",wvar.outfile)
        ConcatNDiff(wvar.outfile,wvar.outfile,d1,d2,"Control","GWaves_fix",diff,dout+wvar.outfile)