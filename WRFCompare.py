import os
from netCDF4 import Dataset
from GetSensVar import *
from wrf import smooth2d
from Plot2DField import *
import imageio
from PIL import Image, ImageDraw

def WRFSmoothDiff(dir_path1,dir_path2,svariable,windbarbs=0,smooth=1,difflabel="",outfile="MyMP4",outdir="./",cleanpng=1):
    #
    print("Comparing WRF files for.",svariable.outfile)
    print("Source wrfout files:",dir_path1," & ",dir_path2)
    print("Using:\n\tdifflabel=",difflabel,
                "\n\twindbarbs=",windbarbs,
                "\n\tsmooth=",smooth,
                "\n\tcleanpng=",cleanpng)
    print("Output will be saved as ",outdir+outfile,"\n")

	#Input check
    svariable.range_min=(svariable.range_min-svariable.range_max)/2
    svariable.range_max=(svariable.range_max-svariable.range_min)/2
	#Need to implement input check here!
    
    # Initialization
    WRFfiles1=[]
    WRFfiles2=[]
    PNGfiles=[]
    vpv1=vpv2=u=v=None
    tmp_dir=outdir+"__"+outfile
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    tmp_dir=tmp_dir+"/"

    # Get list of files from directoy 1
    for file in os.listdir(dir_path1):
        if file.startswith('wrfout'):
            WRFfiles1.append(file)
    WRFfiles1.sort()

    # Get list of files from directoy 2
    for file in os.listdir(dir_path2):
        if file.startswith('wrfout'):
            WRFfiles2.append(file)
    WRFfiles2.sort()

    # Compares list of files
    nfiles=min(len(WRFfiles1),len(WRFfiles2))
    for i in range(nfiles):
        if WRFfiles1[i]!=WRFfiles2[i]:
            print("WARNING!: Files in the two directories may not be compatible.")
            print("The name of these files differs, so they may be simulating different days:")
            print("\t",WRFfiles1[i],"-",WRFfiles2[i])
            print("I will carry on labelling with",WRFfiles1[i],"\b, but make sure you want me to...")

    # Plot each time frame in each file
    for i in range(nfiles):
        # Open the NetCDF files
        wrf_fn_1=WRFfiles1[i]
        wrf_fn_2=WRFfiles2[i]
        wrf_fn=wrf_fn_1
        print("Loading ",wrf_fn_1,"and",wrf_fn_2)
        ncfile1 = Dataset(dir_path1+wrf_fn_1)
        ncfile2 = Dataset(dir_path2+wrf_fn_2)
        # Get number of time frames and plot them
        timerange1=ncfile1.variables['Times'].shape[0]
        timerange2=ncfile2.variables['Times'].shape[0]
        if timerange1!=timerange2:
            print("WARNING!: Files in the two directories may not be compatible.")
            print("The number of time slices differs in the following files:")
            print("\t",WRFfiles1[i],"-",WRFfiles2[i])
            print("This is probably a good time to stop... quitting...")
        else:
            timerange=timerange1
            # for ti in range(0,timerange,4):                              ## For tests only
            for ti in range(timerange):
                of=tmp_dir+outfile+wrf_fn+"_t_"+str(ti)+".png"
                PNGfiles.append(of)
                print("Processing:",ti+1,"/",timerange, end = '\r')
                var1,u1,v1,vpv1=GetSensVar(ncfile1,svariable,windbarbs,ti,vpv1)
                var2,u2,v2,vpv2=GetSensVar(ncfile2,svariable,windbarbs,ti,vpv2)
                if smooth:
                    #Smoothing variables
                    smovar1 = smooth2d(var1, 3, cenweight=4)
                    smovar2 = smooth2d(var2, 3, cenweight=4)
                else:
                    smovar1 = var1
                    smovar2 = var2
                #Making diff
                smooth_var = smooth2d(var1, 3, cenweight=4)
                smooth_var.values = smovar2.values-smovar1.values
                if windbarbs:
                    u=u2-u1
                    v=v2-v1
                #Plotting
                Plot2DField(smooth_var,svariable,windbarbs,of,u,v,smooth=0)
            print("Processed",timerange,"/",timerange,"successfully.")

    if difflabel!="":
        #Adds difflabels to frames
        for i in range(len(PNGfiles)):
            with Image.open(PNGfiles[i]) as im:
                draw = ImageDraw.Draw(im)
                draw.text((10,10),difflabel,fill=(0,0,0))
                im.save(PNGfiles[i])

    # Build mp4
    print("Building MP4 from png files...")
    with imageio.get_writer(outdir+outfile+".mp4", mode='I') as writer:
        for filename in PNGfiles:
            image = imageio.imread(filename)
            writer.append_data(image)

    # Remove individual frame files
    if cleanpng:
        print("Deleting png files...")
        for file in PNGfiles:
            os.remove(file)
        os.removedirs(tmp_dir)
        print("All done.")
