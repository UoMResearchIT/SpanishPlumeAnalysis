import imageio as iio
import numpy as np
from PIL import Image, ImageChops

def ConcatNDiff(dir1="./",file1="f1",dir2="./",file2="f2",diff=1,outfile="vs_f1-f2"):
    
	#Input check
    file1=file1.replace('.mp4','')
    file2=file2.replace('.mp4','')
    outfile=outfile.replace('.mp4','')
    if outfile=="vs_f1-f2": outfile="vs_"+file1+"-"+file2
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

        #Saves mp4 with stitched frames
        with iio.get_writer(outfile+".mp4",format="mp4", mode='I',) as writer:
            for frame in S:
                writer.append_data(frame)
