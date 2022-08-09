import os
import sys
#Adds folder to python path search
sys.path.insert(1, '/mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/')

from Animate import Animate;
import SensibleVariables as sv
from MP4Compare import ConcatNDiff
from WRFCompare import WRFSmoothDiff

import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task',
                        type=str,
                        default="diagnostic",
                        choices=["diagnostic","wrfcompare","mp4compare"])
    parser.add_argument('--var',
                        type=str,
                        default="DewpointTemp2m",
                        help="Sensible variable to work with.",
                        choices=["SeaLevelPressure","AirTemp2m","DewpointTemp2m","RelativeHumidity2m","CAPE","CIN","Rain","AirTemp850","DewpointTemp850","GeoPotHeight500","StaticStability700500","StaticStability850700"])
    parser.add_argument('--windbarbs',
                        type=bool,
                        default=None,
                        help="Default behaviour is set by sensible variable.")
    parser.add_argument('--smooth',
                        type=bool,
                        default=0,
                        help="Set to 1 for conical smoothing of wrf variables.")
    parser.add_argument('--cleanpng',
                        type=bool,
                        default=1,
                        help="Set to 0 to conserve png files generated for the mp4")
    parser.add_argument('--mp4diff',
                        type=bool,
                        default=1,
                        help="If 0 mp4compare simply stitches input files, without making a diff of frames.")
    parser.add_argument('--difflabel',
                        type=str,
                        default="",
                        help="Label added in top corner of diff image")
    parser.add_argument('--label1',
                        type=str,
                        default="Control",
                        help="Label added in top corner of file 1 in mp4 comparison")
    parser.add_argument('--label2',
                        type=str,
                        default="",
                        help="Label added in top corner of file 2 in mp4 comparison")
    parser.add_argument('--dir_path',
                        type=str,
                        default="/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/",
                        help="Path to the directory with your wrfout files.")
    parser.add_argument('--dir1',
                        type=str,
                        default="/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/",
                        help="Path to the directory with your wrfout files to compare against (control).")
    parser.add_argument('--dir2',
                        type=str,
                        default="/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek.half_hgt/",
                        help="Path to the directory with your wrfout files to compare.")
    parser.add_argument('--outdir',
                        type=str,
                        default="./",
                        help="Path to the directory in which outputs will be saved.")
   
    args = parser.parse_args()


match args.var:
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

if args.windbarbs is None:
    windbarbs=wvar.windbarbs
if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)

match args.task:
    case "diagnostic":
        Animate(args.dir_path,wvar,
                windbarbs=windbarbs,
                outfile=wvar.outfile,
                outdir=args.outdir,
                smooth=args.smooth,
                cleanpng=args.cleanpng)
    case "mp4compare":
        ConcatNDiff(wvar.outfile,wvar.outfile,
                    dir1=args.dir1,
                    dir2=args.dir2,
                    label1=args.label1,
                    label2=args.label2,
                    difflabel=args.difflabel,
                    diff=args.mp4diff,
                    outfile=args.outdir+wvar.outfile)
    case "wrfcompare":
        WRFSmoothDiff(args.dir1,args.dir2,wvar,
                      windbarbs=windbarbs,
                      difflabel=args.difflabel,
                      outfile=wvar.outfile,
                      outdir=args.outdir,
                      smooth=args.smooth,
                      cleanpng=args.cleanpng)
