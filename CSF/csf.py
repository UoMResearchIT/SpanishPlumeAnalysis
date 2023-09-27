import os
import sys
#Adds folder to python path search
sys.path.insert(1, '/mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/')

from Animate import Animate;
import SensibleVariables as sv
from MP4Compare import *
from WRFCompare import *

import argparse
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return 1
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return 0
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task',
                        type=str,
                        default="diagnostic",
                        choices=["diagnostic",
                                 "wrfcompare",
                                 "mp4diff",
                                 "mp4stitch"])
    parser.add_argument('--var',
                        type=str,
                        default="DewpointTemp2m",
                        help="Sensible variable to work with.",
                        choices=[
                            "TerrainElevation",
                            "SeaLevelPressure",
                            "AirTemp2m",
                            "DewpointTemp2m",
                            "RelativeHumidity2m",
                            "CAPE",
                            "CIN",
                            "Rain",
                            "SimRadarReflectivityMax",
                            "AirTemp850",
                            "DewpointTemp850",
                            "RelativeHumidity700",
                            "GeoPotHeight500",
                            "StaticStability700500",
                            "StaticStability850700",
                            "SimRadarReflectivity1km",
                        ])
    parser.add_argument('--windbarbs',
                        type=str2bool,
                        default=None,
                        help="Default behaviour is set by sensible variable.")
    parser.add_argument('--smooth',
                        type=str2bool,
                        default=0,
                        help="Set to 1 for conical smoothing of wrf variables.")
    parser.add_argument('--clean',
                        type=str2bool,
                        default=1,
                        help="Set to 0 to conserve png or mp4 temp files generated during the task")
    parser.add_argument('--domain',
                        type=str,
                        default="zoom",
                        choices=["zoom","full"],
                        help="Area to plot, can be the full domain, which includes most of Africa and east Europe, or the zoomed domain, which focuses on North Africa, West Europe and the UK.")
    parser.add_argument('--N',
                        type=int,
                        default=1,
                        help="Number of rows in the grid used for mp4stitch.")
    parser.add_argument('--M',
                        type=int,
                        default=2,
                        help="Number of columns in the grid used for mp4stitch.")
    parser.add_argument('--files',
                        type=str,
                        default="",
                        help="List of file names used for mp4stitch. Provide a list in quotes separated by commas.")
    parser.add_argument('--dirs',
                        type=str,
                        default="",
                        help="List of file directories used for mp4stitch. Provide a list in quotes separated by commas.")
    parser.add_argument('--labels',
                        type=str,
                        default="",
                        help="List of labels used for mp4stitch. Provide a list in quotes separated by commas.")
    parser.add_argument('--colormap',
                        type=str,
                        default=None,
                        help="Default colormaps are defined in sensible variables or the chosen task. You can override them by choosing a different one here.")
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

wvar=eval("sv."+args.var)

if args.windbarbs is None:
    windbarbs=wvar.windbarbs
files=args.files.split(',')
dirs=args.dirs.split(',')
labels=args.labels.split(',')

match args.task:
    case "diagnostic":
        if dirs[0]=="": dir=args.dir_path
        else: dir=dirs[0]
        if wvar==sv.TerrainElevation:
            if dir[-1]!="/":dir=dir+"/"
            outdir=args.outdir
            if outdir[-1]!="/":outdir=outdir+"/"
            WRFfiles=[]
            for file in os.listdir(dir):
                if file.startswith('wrfout'):
                    WRFfiles.append(file)
            WRFfiles.sort()
            var,_,_,_=GetSensVar(Dataset(dir+WRFfiles[0]),wvar)
            of=outdir+wvar.outfile+".png"
            print("Generating diagnostic for",wvar.outfile)
            print("Source wrfout files:",dir)
            print("Using:\n\tdomain=",args.domain,
                        "\n\tsmooth=",args.smooth)
            print("Output will be saved as ",of,"\n")
            Plot2DField(var,wvar,0,of,smooth=args.smooth,domain=args.domain)
        else:
            Animate(dir,wvar,
                    windbarbs=windbarbs,
                    outfile=wvar.outfile,
                    outdir=args.outdir,
                    smooth=args.smooth,
                    domain=args.domain,
                    cleanpng=args.clean)
    case "mp4diff":
        if len(dirs)<2:
            dir1=args.dir1
            dir2=args.dir2
        else:
            dir1=dirs[0]
            dir2=dirs[1]
        if len(labels)<2:
            l1=args.label1,
            l2=args.label2,
        else:
            l1=labels[0]
            l2=labels[1]
        if len(labels)<3:
            dl=args.difflabel
        else:
            dl=labels[2]
        ConcatNDiff(wvar.outfile,wvar.outfile,
                    dir1=dir1,
                    dir2=dir2,
                    label1=l1,
                    label2=l2,
                    difflabel=dl,
                    outfile=wvar.outfile,
                    outdir=args.outdir,
                    cleandiff=args.clean)
    case "mp4stitch":
        ConcatNxM(files,
                  dirs=dirs,
                  labels=labels,
                  N=args.N,
                  M=args.M,
                  outdir=args.outdir)
    case "wrfcompare":
        if len(dirs)<2:
            dir1=args.dir1
            dir2=args.dir2
        else:
            dir1=dirs[0]
            dir2=dirs[1]
        if labels[0]=="": dl=args.difflabel
        else: dl=labels[0]
        WRFSmoothDiff(args.dir1,args.dir2,wvar,
                      windbarbs=windbarbs,
                      difflabel=dl,
                      colormap=args.colormap,
                      outfile=wvar.outfile,
                      outdir=args.outdir,
                      smooth=args.smooth,
                      domain=args.domain,
                      cleanpng=args.clean)
