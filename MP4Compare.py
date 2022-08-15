import os
import imageio as iio
import numpy as np
from PIL import Image, ImageChops, ImageDraw

def ConcatNDiff(file1,file2,dir1="./",dir2="./",label1="",label2="",difflabel="",diff=1,outfile="vs_f1-f2",outdir="./"):
    ##Input check
    #Directories
    if dir1[-1]!="/":dir1=dir1+"/"
    if dir2[-1]!="/":dir2=dir2+"/"
    if outdir[-1]!="/":outdir=outdir+"/"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    #File extensions
    file1=file1.replace('.mp4','')
    file2=file2.replace('.mp4','')
    outfile=outdir+outfile.replace('.mp4','')
    if outfile=="vs_f1-f2": outfile="vs_"+file1+"-"+file2
    #Labels
    if label1+label2=="":labels=0
    else: labels=1

    #
    print("Comparing MP4 files:",dir1+file1," & ",dir2+file2)
    print("Using:\n\t\diff=",diff)
    if labels: print("\tlabels=",label1," & ",label2)
    else: print("\tlabels=None")
    print("Output will be saved as ",outfile,"\n")

	
	#Need to implement input check here!
    
    #Loads images from mp4 files
    MP4_1 = iio.mimread(dir1+file1+'.mp4')
    MP4_2 = iio.mimread(dir2+file2+'.mp4')
    frames=len(MP4_1)
    if frames != len(MP4_2):
        print("The mp4 files dont have the same number of frames.")
    else:
        #Stitches MP4_1 and MP4_2 side by side
        S=np.concatenate((MP4_1,MP4_2),axis=2)

        if diff:
            #Initializes diff image
            MP4_D = [None]*frames
            for i in range(frames):
                #Loads frames  into PIL.Image format
                im1=Image.fromarray(MP4_1[i])
                im2=Image.fromarray(MP4_2[i])
                #Computes pixel by pixel absolute value difference of frames
                farme_diff=ImageChops.difference(im1,im2)
                #farme_diff.show()
                MP4_D[i]=np.array(farme_diff)
            #Stitches MP4_1,MP4_2 and MP4_D side by side
            S=np.concatenate((S,MP4_D),axis=2)

        if labels:
            #Adds labels to frames
            width=np.shape(MP4_1[0])[1]
            for i in range(frames):
                imS=Image.fromarray(S[i])
                draw=ImageDraw.Draw(imS)
                draw.text((10,10),label1,fill=(0,0,0))
                draw.text((10+width,10),label2,fill=(0,0,0))
                draw.text((10+2*width,10),difflabel,fill=(255,255,255))
                S[i]=np.array(imS)

        #Saves mp4 with stitched frames
        with iio.get_writer(outfile+".mp4",format="mp4", mode='I',) as writer:
            for frame in S:
                writer.append_data(frame)

def ConcatNxM(files,dirs=["./","./"],labels=["",""],N=1,M=1,outfile="Concat_NxM",outdir="./"):
    ##Input check
    nfiles=len(files)
    if N*M<nfiles:
        print("Number of files is greater than NxM space. Changing M to fit files.")
        M=int((nfiles+N-1)/N)
    if len(dirs)<nfiles:
        print("Number of directories is less than number of files. Searching for files in cwd.")
        dirs=dirs+["./"]*(nfiles-len(dirs))
    if len(labels)<nfiles:
        labels=labels+[""]*(nfiles-len(labels))

    #Directories and file extensions
    for i in range(nfiles):
        files[i]=files[i].replace('.mp4','')
        files[i]=files[i]+'.mp4'
        if dirs[i][-1]!="/":dirs[i]=dirs[i]+"/"
    if outdir[-1]!="/":outdir=outdir+"/"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if outfile=="Concat_NxM": outfile="Concat_"+str(N)+"x"+str(M)
    outfile=outdir+outfile.replace('.mp4','')
    outfile=outfile+'.mp4'
    files=np.char.add(dirs,files)

    #Verbose
    print("Stitching",nfiles,"MP4 files on",N,"by",M,"grid.")
    print("Source files:\n\t","\n\t ".join(files))
    if ''.join(labels)=="":
        print("No labels are being added.")
    else: print("With labels=\n\t","\n\t ".join(labels))
    print("Output will be saved as ",outfile,"\n")

    #Loads images from mp4 files
    MP4files = [None]*nfiles
    frames = [None]*nfiles
    for i in range(nfiles):
        MP4files[i]=iio.mimread(files[i],memtest=False)
        frames[i]=len(MP4files[i])
    #Only continues if all files have equal number of frames
    if not all(nf == frames[0] for nf in frames):
        print("The mp4 files don't have the same number of frames.")
    else:
        #Processes MP4 files
        blankfile=np.ones(np.shape(MP4files[0][0]), dtype=np.uint8)*255
        height=np.shape(MP4files[0])[1]
        width=np.shape(MP4files[0])[2]
        with iio.get_writer(outfile,format="mp4", mode='I',) as writer:
            for idx in range(frames[0]):
                #Stitches MP4 files in NxM grid
                for r in range(N):
                    R=MP4files[r*M][idx]
                    for c in range(1,M):
                        if r*M+c<nfiles:
                            R=np.concatenate((R,MP4files[r*M+c][idx]),axis=1)
                        else:
                            R=np.concatenate((R,blankfile),axis=1)
                    if r==0:
                        Sframe=R
                    else:
                        Sframe=np.concatenate((Sframe,R),axis=0)

                #Adds labels if present
                if ''.join(labels)!="":
                    imS=Image.fromarray(Sframe)
                    draw=ImageDraw.Draw(imS)
                    for r in range(N):
                        for c in range(M):
                            if r*M+c<nfiles:
                                draw.text((10+c*width,10+r*height),labels[r*M+c],fill=(0,0,0))
                    Sframe=np.array(imS)

                #Saves mp4 with stitched frames
                writer.append_data(Sframe)