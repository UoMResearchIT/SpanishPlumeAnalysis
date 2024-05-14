import os
import sys

# Adds folder to python path search
sys.path.insert(1, "/".join(__file__.split("/")[:-2]))

from Animate import Animate
from TerrainPlots import Terrain
from CSV_Data import CSV_Data
import SensibleVariables as sv
from MP4Compare import *
from WRFCompare import *

import argparse


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return 1
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return 0
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--task",
        type=str,
        default="diagnostic",
        choices=["diagnostic", "csv", "wrfcompare", "mp4diff", "mp4stitch"],
    )
    parser.add_argument(
        "--var",
        type=str,
        default="DewpointTemp2m",
        help="Sensible variable to work with.",
    )
    parser.add_argument(
        "--windbarbs",
        type=str2bool,
        default=None,
        help="Default behaviour is set by sensible variable.",
    )
    parser.add_argument(
        "--smooth",
        type=str2bool,
        default=0,
        help="Set to 1 for conical smoothing of wrf variables.",
    )
    parser.add_argument(
        "--clean",
        type=str2bool,
        default=1,
        help="Set to 0 to conserve png or mp4 temp files generated during the task",
    )
    parser.add_argument(
        "--save_pdf_frames",
        type=str2bool,
        default=0,
        help="Set to 1 to save pdf files of each frame generated during the task",
    )
    parser.add_argument(
        "--domain",
        type=str,
        default="zoom",
        choices=["zoom", "full"],
        help="Area to plot, can be the full domain, which includes most of Africa and east Europe, or the zoomed domain, which focuses on North Africa, West Europe and the UK.",
    )
    parser.add_argument(
        "--N",
        type=int,
        default=1,
        help="Number of rows in the grid used for mp4stitch.",
    )
    parser.add_argument(
        "--M",
        type=int,
        default=2,
        help="Number of columns in the grid used for mp4stitch.",
    )
    parser.add_argument(
        "--files",
        type=str,
        default="",
        help="List of file names used for mp4stitch. Provide a list in quotes separated by commas.",
    )
    parser.add_argument(
        "--dirs",
        type=str,
        default="",
        help="List of file directories used for mp4stitch. Provide a list in quotes separated by commas.",
    )
    parser.add_argument(
        "--labels",
        type=str,
        default="",
        help="List of labels used for mp4stitch. Provide a list in quotes separated by commas.",
    )
    parser.add_argument(
        "--colormap",
        type=str,
        default=None,
        help="Default colormaps are defined in sensible variables or the chosen task. You can override them by choosing a different one here.",
    )
    parser.add_argument(
        "--range_min",
        type=str,
        default=None,
        help="Minimum value used in the colormap. Default value is defined in sensible variables. You can override them by choosing a different one here.",
    )
    parser.add_argument(
        "--range_max",
        type=str,
        default=None,
        help="Maximum value used in the colormap. Default value is defined in sensible variables. You can override them by choosing a different one here.",
    )
    parser.add_argument(
        "--difflabel",
        type=str,
        default="",
        help="Label added in top corner of diff image",
    )
    parser.add_argument(
        "--label1",
        type=str,
        default="Control",
        help="Label added in top corner of file 1 in mp4 comparison",
    )
    parser.add_argument(
        "--label2",
        type=str,
        default="",
        help="Label added in top corner of file 2 in mp4 comparison",
    )
    parser.add_argument(
        "--dir_path",
        type=str,
        default="/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/",
        help="Path to the directory with your wrfout files.",
    )
    parser.add_argument(
        "--dir1",
        type=str,
        default="/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/",
        help="Path to the directory with your wrfout files to compare against (control).",
    )
    parser.add_argument(
        "--dir2",
        type=str,
        default="/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek.half_hgt/",
        help="Path to the directory with your wrfout files to compare.",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default="./",
        help="Path to the directory in which outputs will be saved.",
    )
    parser.add_argument(
        "--file_tag",
        type=str,
        default="",
        help="Tag appended at the end of the output file name to prevent replacement.",
    )
    parser.add_argument(
        "--lat",
        type=str,
        default=None,
        help="Latitude of point of interest (used for SkewT plots).",
    )
    parser.add_argument(
        "--lon",
        type=str,
        default=None,
        help="Longitude of point of interest (used for SkewT plots).",
    )
    parser.add_argument(
        "--place",
        type=str,
        default=None,
        help="Name of place for point location on map).",
        choices=[attr.split("_")[1] for attr in dir(sv) if attr.startswith("SkewT_")],
    )

    args = parser.parse_args()

var_choices = [
    attr
    for attr in dir(sv)
    if not callable(getattr(sv, attr)) and not attr.startswith("__")
]
if "," not in args.var:
    if "CSV_" in args.var:
        if args.place is None and (args.lat is None or args.lon is None):
            s = args.var.split("_")
            if s[1]:
                args.place = s[1]
        csv_data_v = ["AirTemp", "DewpointTemp", "RelativeHumidity"]
        csv_data_p = [925, 850, 700, 500, 300]
        csv_data_svars = ["CIN", "CAPE"] + [
            f"{var}{height}" for var in csv_data_v for height in csv_data_p
        ]
        args.var = ",".join(csv_data_svars)
        print(args.var)
    else:
        if args.var not in var_choices:
            print(f"Variable {args.var} not found in SensibleVariables.py.")
            print(f"Please choose from {var_choices}.")
            raise ValueError("Incorrect value passed to --var.")
        wvar = eval("sv." + args.var)
if "," in args.var:
    args.var = args.var.split(",")
    incorrect_var = False
    for var in args.var:
        if var not in var_choices:
            incorrect_var = True
            print(f"Variable {var} not found in SensibleVariables.py.")
    if incorrect_var:
        print(f"Please choose from {var_choices}.")
        raise ValueError("Incorrect value passed to --var.")
    wvars = [eval("sv." + var) for var in args.var]
    wvar = sv.SkewT
    wvar.outfile = "CSV_Data"
if args.range_min is not None:
    wvar.range_min = float(args.range_min)
if args.range_max is not None:
    wvar.range_max = float(args.range_max)

if args.place is not None:
    tmpsv = eval("sv.SkewT_" + args.place)
    wvar.lat = tmpsv.lat
    wvar.lon = tmpsv.lon
if args.lat is not None:
    wvar.lat = float(args.lat)
if args.lon is not None:
    wvar.lon = float(args.lon)
if "SkewT" in wvar.outfile and (args.lat is not None or args.lon is not None):
    wvar.outfile = f"SkewT_at_{wvar.lat}_{wvar.lon}"
    wvar.ptitle = f"SkewT at {wvar.lat},{wvar.lon}"
if "CSV_Data" in wvar.outfile:
    if args.place is None:
        wvar.outfile = f"CSV_Data_{wvar.lat},{wvar.lon}"
    else:
        wvar.outfile = f"CSV_Data_{args.place}"

if args.windbarbs is None:
    windbarbs = wvar.windbarbs
files = args.files.split(",")
dirs = args.dirs.split(",")
labels = args.labels.split(",")
outfile = wvar.outfile + args.file_tag

match args.task:
    case "diagnostic":
        if dirs[0] == "":
            dir = args.dir_path
        else:
            dir = dirs[0]
        if wvar == sv.TerrainElevation or wvar == sv.TerrainElevation1000:
            Terrain(
                dir,
                wvar,
                outfile=outfile,
                outdir=args.outdir,
                smooth=args.smooth,
                domain=args.domain,
            )
        else:
            Animate(
                dir,
                wvar,
                windbarbs=windbarbs,
                outfile=outfile,
                outdir=args.outdir,
                smooth=args.smooth,
                domain=args.domain,
                cleanpng=args.clean,
                save_pdf=args.save_pdf_frames,
            )
    case "csv":
        CSV_Data(
            args.dir_path,
            wvars,
            location=wvar,
            outfile=outfile,
            outdir=args.outdir,
            domain=args.domain,
        )
    case "mp4diff":
        if len(dirs) < 2:
            dir1 = args.dir1
            dir2 = args.dir2
        else:
            dir1 = dirs[0]
            dir2 = dirs[1]
        if len(labels) < 2:
            l1 = (args.label1,)
            l2 = (args.label2,)
        else:
            l1 = labels[0]
            l2 = labels[1]
        if len(labels) < 3:
            dl = args.difflabel
        else:
            dl = labels[2]
        ConcatNDiff(
            wvar.outfile,
            wvar.outfile,
            dir1=dir1,
            dir2=dir2,
            label1=l1,
            label2=l2,
            difflabel=dl,
            outfile=outfile,
            outdir=args.outdir,
            cleandiff=args.clean,
        )
    case "mp4stitch":
        ConcatNxM(
            files, dirs=dirs, labels=labels, N=args.N, M=args.M, outdir=args.outdir
        )
    case "wrfcompare":
        if len(dirs) < 2:
            dir1 = args.dir1
            dir2 = args.dir2
        else:
            dir1 = dirs[0]
            dir2 = dirs[1]
        if labels[0] == "":
            dl = args.difflabel
        else:
            dl = labels[0]
        WRFSmoothDiff(
            args.dir1,
            args.dir2,
            wvar,
            windbarbs=windbarbs,
            difflabel=dl,
            colormap=args.colormap,
            outfile=outfile,
            outdir=args.outdir,
            smooth=args.smooth,
            domain=args.domain,
            cleanpng=args.clean,
            save_pdf=args.save_pdf_frames,
        )
