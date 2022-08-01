class wrf_var:
	def __init__(self, dim=3, wrfname=None, ptitle=None, outfile=None, range_min=None, range_max=None,interpvar="pressure",interpvalue=None):
		self.dim = dim
		self.wrfname = wrfname
		self.ptitle = ptitle
		self.outfile = outfile
		self.range_min = range_min
		self.range_max = range_max
		self.interpvar = interpvar
		self.interpvalue = interpvalue


SeaLevelPressure = wrf_var(3,"slp","Sea level pressure [hPa]","SeaLevelPressure",985,1035)
AirTemp2m = wrf_var(3,"T2","Temperature at 2m [K]","AirTemp2m",270,330)
DewpointTemp2m = wrf_var(3,"td2","Dewpoint Temperature at 2m [C]","DewpointTemp2m",-20,35)
RelativeHumidity2m = wrf_var(3,"rh2","Relative Humidity at 2m [%]","RelHum2m",0,100)

Pressure = wrf_var(4,"pressure","Pressure [hPa]","Pressure",500,1500)

AirTemp850 = wrf_var(4,"temp","Temperature at 850 hPa [K]","AirTemp850",270,310,"pressure",850)
DewpointTemp850 = wrf_var(4,"td","Dewpoint Temperature at 850hPa [C]","DewpointTemp850",-30,30,"pressure",850)