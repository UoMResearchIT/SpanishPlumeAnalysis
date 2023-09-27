from matplotlib.cm import get_cmap
from matplotlib.colors import ListedColormap

class svariable:
	def __init__(self, dim=3, wrfname=None, ptitle=None, outfile=None, range_min=None, range_max=None,interpvar="pressure",interpvalue=None,windbarbs=0,isdif=0,colormap=get_cmap("jet"),scale="linear",numloglevs=10,logbase=10,bounds=None):
		self.dim = dim
		self.wrfname = wrfname
		self.ptitle = ptitle
		self.outfile = outfile
		self.range_min = range_min
		self.range_max = range_max
		self.interpvar = interpvar
		self.interpvalue = interpvalue
		self.windbarbs = windbarbs
		self.isdif = isdif
		self.colormap = colormap
		self.scale=scale
		self.numloglevs=numloglevs
		self.logbase=logbase
		self.bounds=bounds

# 2D + Field
TerrainElevation = svariable(wrfname="ter",
						   ptitle="Terrain elevation [m]",
						   outfile="TerrainElevation",
						   range_min=0,
						   range_max=2000,
						   colormap=get_cmap("terrain"))
SeaLevelPressure = svariable(wrfname="slp",
						   ptitle="Sea level pressure [hPa]",
						   outfile="SeaLevelPressure",
						   range_min=990,
						   range_max=1030,
						   windbarbs=1,
			   			   colormap=get_cmap("Purples"))
AirTemp2m = svariable(wrfname="T2",
					ptitle="Temperature at 2m [K]",
					outfile="AirTemp2m",
					range_min=270,
					range_max=330,
			   		colormap=get_cmap("Reds"))
DewpointTemp2m = svariable(wrfname="td2",
						 ptitle="Dewpoint Temperature at 2m [C]",
						 outfile="DewpointTemp2m",
						 range_min=-21,
						 range_max=35,
			   			 colormap=get_cmap("BuPu"))
RelativeHumidity2m = svariable(wrfname="rh2",
							 ptitle="Relative Humidity at 2m [%]",
							 outfile="RelHum2m",
							 range_min=0,
							 range_max=100,
			   				 colormap=get_cmap("YlGnBu"))
CAPE = svariable(wrfname="cape_2d",
			   ptitle="Max CAPE (Convective Available Potential Energy) [J/kg]",
			   outfile="CAPE",
			#    range_min=0,
			#    range_max=6000,
			#    colormap=get_cmap("BuGn"))
			   scale="bounds",
			   colormap = ListedColormap(["white","cyan","cornflowerblue","blue",
			   									"lawngreen","limegreen","green","darkgreen",
												"yellow","gold","darkorange","red",
												"firebrick","darkred","magenta","darkviolet",
												"bisque"]),
			   bounds=[-0.1,0,10,50,100,150,200,300,400,500,750,1000,1500,2000,3000,4000,5000,6000],
			   range_min=0,
			   range_max=6000)
CIN = svariable(wrfname="cape_2d",
			   ptitle="Max CIN (Convective Inhibition) [J/kg]",
			   outfile="CIN",
			#    range_min=0,
			#    range_max=1600,
			#    colormap=get_cmap("BuGn"))
			   scale="bounds",
			   colormap = ListedColormap(["white","cyan","cornflowerblue","blue",
			   									"lawngreen","limegreen","green","darkgreen",
												"yellow","gold","darkorange","red",
												"firebrick","darkred"]),
			   bounds=[-0.1,0,10,50,100,150,200,300,400,500,750,1000,1500,2000,3000],
			   range_min=0,
			   range_max=3000)
Rain = svariable(wrfname="RAINC",
			   ptitle="Total Hourly Precipitation [mm]",
			   outfile="Rain",
			   windbarbs=1,
			   isdif=1,
			#    scale="linear",
			#    colormap=get_cmap("Blues"),
			#    range_min=0,
			#    range_max=12)
			   scale="log",
			   colormap = ListedColormap(["white","blue","blue","darkgreen","gold","darkorange","red","magenta","cyan"]),
			   numloglevs=10,
			   logbase=2,
			   range_min=-3,
			   range_max=6)
			#    scale="bounds",
			#    colormap = ListedColormap(["white","cyan","cornflowerblue","blue",
			#    									"lawngreen","limegreen","green","darkgreen",
			# 									"yellow","gold","darkorange","red",
			# 									"firebrick","darkred","magenta","darkviolet",
			# 									"bisque"]),
			#    bounds=[-0.1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
			#    range_min=0,
			#    range_max=16)
SimRadarReflectivityMax = svariable(wrfname="mdbz",
								ptitle="Maximum simulated radar reflectivity[dBZ]",
								outfile="SimRadarReflMax",
								windbarbs=1,
								scale="bounds",
								colormap = ListedColormap(["white",
											    "cyan","deepskyblue","blue",
			   									"steelblue","lawngreen","green",
												"gold","darkorange","red",
												"firebrick","darkred","indigo",
												"rebeccapurple","mediumpurple","lavender"]),
								bounds=[-0.1,0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75],
								range_min=0,
								range_max=64)

# 3D + Field
AirTemp850 = svariable(dim=4,
					 wrfname="temp",
					 ptitle="Temperature at 850 hPa [K]",
					 outfile="AirTemp850",
					 range_min=270,range_max=314,
					 interpvar="pressure",
					 interpvalue=850,
					 colormap=get_cmap("Reds"))
AirTemp500 = svariable(dim=4,
					 wrfname="temp",
					 ptitle="Temperature at 500 hPa [K]",
					 outfile="AirTemp500",
					 range_min=240,range_max=280,
					 interpvar="pressure",
					 interpvalue=500,
					 colormap=get_cmap("Reds"))
AirTemp850Dif6h = svariable(dim=4,
					 wrfname="temp",
					 ptitle="Temperature change in 6h at 850 hPa [K]",
					 outfile="AirTemp850Dif6h",
					 range_min=-20,range_max=20,
					 interpvar="pressure",
					 interpvalue=850,
					 colormap=get_cmap("Reds"))
AirTemp700Dif6h = svariable(dim=4,
					 wrfname="temp",
					 ptitle="Temperature change in 6h at 700 hPa [K]",
					 outfile="AirTemp700Dif6h",
					 range_min=-20,range_max=20,
					 interpvar="pressure",
					 interpvalue=700,
					 colormap=get_cmap("Reds"))
AirTemp500Dif6h = svariable(dim=4,
					 wrfname="temp",
					 ptitle="Temperature change in 6h at 500 hPa [K]",
					 outfile="AirTemp500Dif6h",
					 range_min=-20,range_max=20,
					 interpvar="pressure",
					 interpvalue=500,
					 colormap=get_cmap("Reds"))
AirTemp850Dif12h = svariable(dim=4,
					 wrfname="temp",
					 ptitle="Temperature change in 12h at 850 hPa [K]",
					 outfile="AirTemp850Dif12h",
					 range_min=-20,range_max=20,
					 interpvar="pressure",
					 interpvalue=850,
					 colormap=get_cmap("Reds"))
AirTemp700Dif12h = svariable(dim=4,
					 wrfname="temp",
					 ptitle="Temperature change in 12h at 700 hPa [K]",
					 outfile="AirTemp700Dif12h",
					 range_min=-20,range_max=20,
					 interpvar="pressure",
					 interpvalue=700,
					 colormap=get_cmap("Reds"))
AirTemp500Dif12h = svariable(dim=4,
					 wrfname="temp",
					 ptitle="Temperature change in 12h at 500 hPa [K]",
					 outfile="AirTemp500Dif12h",
					 range_min=-20,range_max=20,
					 interpvar="pressure",
					 interpvalue=500,
					 colormap=get_cmap("Reds"))
DewpointTemp850 = svariable(dim=4,
						  wrfname="td",
						  ptitle="Dewpoint Temperature at 850hPa [C]",
						  outfile="DewpointTemp850",
						  range_min=-75,
						  range_max=25,
						  interpvar="pressure",
						  interpvalue=850,
			   			  colormap=get_cmap("BuPu"))
RelativeHumidity700 = svariable(dim=4,
							wrfname="rh",
							ptitle="Relative Humidity at 700hPa [%]",
							outfile="RelHum700",
							range_min=0,
							range_max=100,
							interpvar="pressure",
						  	interpvalue=700,
			   				colormap=get_cmap("YlGnBu"))
GeoPotHeight500 = svariable(dim=4,
						  ptitle="Geopotential Height at 500hPa [m]",
						  outfile="GeoPotHeight500",
						  range_min=5350,
						  range_max=6050,
						  windbarbs=1,
						  interpvar="pressure",
						  interpvalue=500,
			   			  colormap=get_cmap("Greens"))
StaticStability700500 = svariable(dim=4,
								wrfname="temp",
								ptitle="Static stability at 700-500 hPa [C]",
								outfile="StaticStability700500",
								range_min=5,
								range_max=30,
								interpvar="pressure",
								interpvalue=700,
			   			 		colormap=get_cmap("Oranges"))
StaticStability850700 = svariable(dim=4,
								wrfname="temp",
								ptitle="Static stability at 850-700 hPa [C]",
								outfile="StaticStability850700",
								range_min=-5,
								range_max=23,
								interpvar="pressure",
								interpvalue=700,
			   			 		colormap=get_cmap("Oranges"))
SimRadarReflectivity1km = svariable(dim=4,
								wrfname="dbz",
								ptitle="Simulated radar reflectivity at 1km [dBZ]",
								outfile="SimRadarRefl1km",
								interpvar="z",
								interpvalue=1000,
								windbarbs=1,
								scale="bounds",
								colormap = ListedColormap(["white",
											    "cyan","deepskyblue","blue",
			   									"steelblue","lawngreen","green",
												"gold","darkorange","red",
												"firebrick","darkred","indigo",
												"rebeccapurple","mediumpurple","lavender"]),
								bounds=[-0.1,0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75],
								range_min=0,
								range_max=64)
