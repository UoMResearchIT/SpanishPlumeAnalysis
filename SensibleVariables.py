class svariable:
	def __init__(self, dim=3, wrfname=None, ptitle=None, outfile=None, range_min=None, range_max=None,interpvar="pressure",interpvalue=None,windbarbs=0,isdif=0):
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

# 2D + Field
SeaLevelPressure = svariable(wrfname="slp",
						   ptitle="Sea level pressure [hPa]",
						   outfile="SeaLevelPressure",
						   range_min=980,
						   range_max=1035,
						   windbarbs=1)
AirTemp2m = svariable(wrfname="T2",
					ptitle="Temperature at 2m [K]",
					outfile="AirTemp2m",
					range_min=270,
					range_max=330)
DewpointTemp2m = svariable(wrfname="td2",
						 ptitle="Dewpoint Temperature at 2m [C]",
						 outfile="DewpointTemp2m",
						 range_min=-20,
						 range_max=35)
RelativeHumidity2m = svariable(wrfname="rh2",
							 ptitle="Relative Humidity at 2m [%]",
							 outfile="RelHum2m",
							 range_min=0,
							 range_max=100)
CAPE = svariable(wrfname="cape_2d",
			   ptitle="Max CAPE (Convective Available Potential Energy) [J/kg]",
			   outfile="CAPE",
			   range_min=0,
			   range_max=6000)
CIN = svariable(wrfname="cape_2d",
			   ptitle="Max CIN (Convective Inhibition) [J/kg]",
			   outfile="CIN",
			   range_min=0,
			   range_max=1600)
Rain = svariable(wrfname="RAINC",
			   ptitle="Total Hourly Precipitation [mm]",
			   outfile="Rain",
			   range_min=0,
			   range_max=30,
			   windbarbs=1,
			   isdif=1)

# 3D + Field
AirTemp850 = svariable(dim=4,
					 wrfname="temp",
					 ptitle="Temperature at 850 hPa [K]",
					 outfile="AirTemp850",
					 range_min=265,range_max=315,
					 interpvar="pressure",
					 interpvalue=850)
DewpointTemp850 = svariable(dim=4,
						  wrfname="td",
						  ptitle="Dewpoint Temperature at 850hPa [C]",
						  outfile="DewpointTemp850",
						  range_min=-80,
						  range_max=25,
						  interpvar="pressure",
						  interpvalue=850)
GeoPotHeight500 = svariable(dim=4,
						  ptitle="Geopotential Height at 500hPa [m]",
						  outfile="GeoPotHeight500",
						  range_min=5350,
						  range_max=6050,
						  windbarbs=1,
						  interpvar="pressure",
						  interpvalue=500)
StaticStability700500 = svariable(dim=4,
								wrfname="temp",
								ptitle="Static stability at 700-500 hPa [C]",
								outfile="StaticStability700500",
								range_min=5,
								range_max=30,
								interpvar="pressure",
								interpvalue=700)
StaticStability850700 = svariable(dim=4,
								wrfname="temp",
								ptitle="Static stability at 850-700 hPa [C]",
								outfile="StaticStability850700",
								range_min=-5,
								range_max=20,
								interpvar="pressure",
								interpvalue=700)