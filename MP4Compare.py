import imageio as iio
import numpy as np
from PIL import Image, ImageChops, ImageDraw

def ConcatNDiff(file1,file2,dir1="./",dir2="./",label1="",label2="",difflabel="",diff=1,outfile="vs_f1-f2"):
    #Input check
    file1=file1.replace('.mp4','')
    file2=file2.replace('.mp4','')
    outfile=outfile.replace('.mp4','')
    if outfile=="vs_f1-f2": outfile="vs_"+file1+"-"+file2
    if label1+label2=="":labels=0
    else: labels=1

    #
    print("Comparing MP4 files:",dir1+file1," & ",dir2+file2)
    print("Using:\n\diff=",diff)
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
                draw.text((10+2*width,10),difflabel,fill=(0,0,0))
                S[i]=np.array(imS)

        #Saves mp4 with stitched frames
        with iio.get_writer(outfile+".mp4",format="mp4", mode='I',) as writer:
            for frame in S:
                writer.append_data(frame)
