from GetSensVar import *
from Plot2DField import *
import os

def Terrain(dir_path,svariable,outfile="MyTerrain",outdir="./",smooth=1,domain="zoom"):

    ##Input check
    #Directories
    if dir_path[-1]!="/":dir_path=dir_path+"/"
    if outdir[-1]!="/":outdir=outdir+"/"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    of=outdir+outfile+".png"
	#Need to implement input check here!

    #
    print("Generating diagnostic for",svariable.outfile)
    print("Source wrfout files:",dir_path)
    print("Using:\n\tdomain =",domain,
                "\n\tsmooth    =",smooth)
    print("Output will be saved as ",of,"\n")

    # Get list of files from directoy
    WRFfiles=[]
    for file in os.listdir(dir_path):
        if file.startswith('wrfout'):
            WRFfiles.append(file)
    WRFfiles.sort()
    ncfile=Dataset(dir_path+WRFfiles[0])
    var,_,_,_=GetSensVar(ncfile,svariable)

    Plot2DField(var,svariable,0,of,smooth=smooth,domain=domain,nlevs=11)
