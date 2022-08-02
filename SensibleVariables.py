class wrf_var:
	def __init__(self, dim=3, wrfname=None, ptitle=None, outfile=None, range_min=None, range_max=None,interpvar="pressure",interpvalue=None,windbarbs=0):
		self.dim = dim
		self.wrfname = wrfname
		self.ptitle = ptitle
		self.outfile = outfile
		self.range_min = range_min
		self.range_max = range_max
		self.interpvar = interpvar
		self.interpvalue = interpvalue
		self.windbarbs = windbarbs

# 2D + Field
SeaLevelPressure = wrf_var(wrfname="slp",
						   ptitle="Sea level pressure [hPa]",
						   outfile="SeaLevelPressure",
						   range_min=980,
						   range_max=1035,
						   windbarbs=1)
AirTemp2m = wrf_var(wrfname="T2",
					ptitle="Temperature at 2m [K]",
					outfile="AirTemp2m",
					range_min=270,
					range_max=330)
DewpointTemp2m = wrf_var(wrfname="td2",
						 ptitle="Dewpoint Temperature at 2m [C]",
						 outfile="DewpointTemp2m",
						 range_min=-20,
						 range_max=35)
RelativeHumidity2m = wrf_var(wrfname="rh2",
							 ptitle="Relative Humidity at 2m [%]",
							 outfile="RelHum2m",
							 range_min=0,
							 range_max=100)
CAPE = wrf_var(wrfname="cape_2d",
			   ptitle="Max CAPE (Convective Available Potential Energy) [J/kg]",
			   outfile="CAPE",
			   range_min=0,
			   range_max=4000)
CIN = wrf_var(wrfname="cape_2d",
			   ptitle="Max CIN (Convective Inhibition) [J/kg]",
			   outfile="CIN",
			   range_min=0,
			   range_max=1000)

# 3D + Field
AirTemp850 = wrf_var(dim=4,
					 wrfname="temp",
					 ptitle="Temperature at 850 hPa [K]",
					 outfile="AirTemp850",
					 range_min=265,range_max=315,
					 interpvar="pressure",
					 interpvalue=850)
DewpointTemp850 = wrf_var(dim=4,
						  wrfname="td",
						  ptitle="Dewpoint Temperature at 850hPa [C]",
						  outfile="DewpointTemp850",
						  range_min=-45,
						  range_max=25,
						  interpvar="pressure",
						  interpvalue=850)
GeoPotHeight500 = wrf_var(dim=4,
						  ptitle="Geopotential Height at 500hPa [m]",
						  outfile="GeoPotHeight500",
						  range_min=5300,
						  range_max=6100,
						  windbarbs=1,
						  interpvar="pressure",
						  interpvalue=500)