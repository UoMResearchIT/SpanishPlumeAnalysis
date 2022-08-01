class wrf_var:
	def __init__(self, wrfname, ptitle, outfile, range_min, range_max):
		self.wrfname = wrfname
		self.ptitle = ptitle
		self.outfile = outfile
		self.range_min = range_min
		self.range_max = range_max


SeaLevelPressure = wrf_var("slp","Sea level pressure [hPa]","SeaLevelPressure",985,1035)
AirTemp2m = wrf_var("T2","Temperature at 2m [K]","AirTemp2m",270,330)
DewpointTemp2m = wrf_var("td2","Dewpoint Temperature at 2m [C?]","DewpointTemp2m",-20,35)
RelativeHumidity2m = wrf_var("rh2","Relative Humidity at 2m [%]","RelHum2m",0,100)