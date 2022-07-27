from Plot2DField import *
import imageio

Files=[]
for time in range(24):
	of="t_"+str(time)+".png"
	Files.append(of)
	Plot2DField("slp","Sea level pressure [hPa] - t="+str(time),time,of)

# Build GIF
with imageio.get_writer('SLP.gif', mode='I') as writer:
    for filename in Files:
        image = imageio.imread(filename)
        writer.append_data(image)