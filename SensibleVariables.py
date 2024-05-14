from matplotlib.cm import get_cmap
from matplotlib.colors import ListedColormap
import cmasher as cmr


class svariable:
    def __init__(
        self,
        dim=3,
        wrfname=None,
        ptitle=None,
        outfile=None,
        range_min=None,
        range_max=None,
        interpvar="pressure",
        interpvalue=None,
        windbarbs=0,
        isdif=0,
        colormap=get_cmap("jet"),
        contour_color=None,
        contour_c_labels=True,
        scale="linear",
        nticks=5,
        nlevs=9,
        logbase=10,
        bounds=None,
        hide_edge_ticks=True,
        overlap_sv=None,
        overlap_gap=None,
        overlap_cmap=None,
        lat=None,
        lon=None,
    ):
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
        self.contour_color = contour_color
        self.contour_c_labels = contour_c_labels
        self.scale = scale
        self.nticks = nticks
        self.nlevs = nlevs
        self.logbase = logbase
        self.bounds = bounds
        self.hide_edge_ticks = hide_edge_ticks
        self.overlap_sv = overlap_sv
        self.overlap_gap = overlap_gap
        self.overlap_cmap = overlap_cmap
        self.lat = lat
        self.lon = lon


# 2D + Field
TerrainElevation = svariable(
    wrfname="ter",
    ptitle="Terrain elevation [m]",
    outfile="TerrainElevation",
    range_min=-200,
    range_max=2000,
    colormap=ListedColormap(
        [
            "mediumblue",
            "darkgreen",
            "green",
            "limegreen",
            "lawngreen",
            "yellow",
            "gold",
            "sienna",
            "burlywood",
            "linen",
            "white",
        ]
    ),
    scale="bounds",
    bounds=[
        -0.05,
        1,
        200,
        400,
        600,
        800,
        1000,
        1200,
        1400,
        1600,
        1800,
        2000,
    ],
)
TerrainElevation1000 = svariable(
    wrfname="ter",
    ptitle="Terrain elevation [m]",
    outfile="TerrainElevation",
    range_min=-100,
    range_max=1000,
    colormap=ListedColormap(
        [
            "mediumblue",
            "darkgreen",
            "green",
            "limegreen",
            "lawngreen",
            "yellow",
            "gold",
            "sienna",
            "burlywood",
            "linen",
            "white",
        ]
    ),
    scale="bounds",
    bounds=[
        -0.05,
        1,
        100,
        200,
        300,
        400,
        500,
        600,
        700,
        800,
        900,
        1000,
    ],
)
SeaLevelPressure = svariable(
    wrfname="slp",
    ptitle="Sea level pressure [hPa]",
    outfile="SeaLevelPressure",
    nticks=12,
    nlevs=12,
    range_min=986,
    range_max=1030,
    windbarbs=1,
    colormap=get_cmap("Purples"),
)
SeaLevelPressure1hPa = svariable(
    wrfname="slp",
    ptitle="Sea level pressure [hPa]",
    outfile="SeaLevelPressure1hPa",
    range_min=986,
    range_max=1030,
    nticks=12,
    nlevs=45,
    windbarbs=1,
    colormap=get_cmap("Purples"),
    contour_color="navy",
)
SeaLevelPressure2hPa = svariable(
    wrfname="slp",
    ptitle="Sea level pressure [hPa]",
    outfile="SeaLevelPressure2hPa",
    range_min=986,
    range_max=1030,
    nticks=12,
    nlevs=23,
    windbarbs=1,
    colormap=get_cmap("Purples"),
    contour_color="navy",
)
AirTemp2m = svariable(
    wrfname="T2",
    ptitle="Temperature at 2m [K]",
    outfile="AirTemp2m",
    nticks=11,
    nlevs=61,
    range_min=270,
    range_max=330,
    colormap=get_cmap("Reds"),
    contour_color="maroon",
)
DewpointTemp2m = svariable(
    wrfname="td2",
    ptitle="Dewpoint Temperature at 2m [C]",
    outfile="DewpointTemp2m",
    nticks=12,
    nlevs=56,
    range_min=-20,
    range_max=35,
    colormap=get_cmap("BuPu"),
    contour_color="indigo",
)
RelativeHumidity2m = svariable(
    wrfname="rh2",
    ptitle="Relative Humidity at 2m [%]",
    outfile="RelHum2m",
    range_min=0,
    range_max=100,
    colormap=get_cmap("YlGnBu"),
)
PotentialTemp2m = svariable(
    wrfname="TH2",
    ptitle="Potential temperature at 2m [K]",
    outfile="PotTemp2m",
    nticks=11,
    nlevs=21,
    range_min=280,
    range_max=320,
    colormap=get_cmap("Reds"),
)
CAPE = svariable(
    wrfname="cape_2d",
    ptitle="Max CAPE (Convective Available Potential Energy) [J/kg]",
    outfile="CAPE",
    #    range_min=0,
    #    range_max=6000,
    #    colormap=get_cmap("BuGn"))
    scale="bounds",
    colormap=ListedColormap(
        [
            "white",
            "cyan",
            "cornflowerblue",
            "blue",
            "lawngreen",
            "limegreen",
            "green",
            "darkgreen",
            "yellow",
            "gold",
            "darkorange",
            "red",
            "firebrick",
            "darkred",
            "magenta",
            "darkviolet",
            "bisque",
        ]
    ),
    bounds=[
        -0.1,
        0,
        10,
        50,
        100,
        150,
        200,
        300,
        400,
        500,
        750,
        1000,
        1500,
        2000,
        3000,
        4000,
        5000,
        6000,
    ],
    range_min=0,
    range_max=6000,
)
CIN = svariable(
    wrfname="cape_2d",
    ptitle="Max CIN (Convective Inhibition) [J/kg]",
    outfile="CIN",
    #    range_min=0,
    #    range_max=1600,
    #    colormap=get_cmap("BuGn"))
    scale="bounds",
    colormap=ListedColormap(
        [
            "white",
            "cyan",
            "cornflowerblue",
            "blue",
            "lawngreen",
            "limegreen",
            "green",
            "darkgreen",
            "yellow",
            "gold",
            "darkorange",
            "red",
            "firebrick",
            "darkred",
        ]
    ),
    bounds=[-0.1, 0, 10, 50, 100, 150, 200, 300, 400, 500, 750, 1000, 1500, 2000, 3000],
    range_min=0,
    range_max=3000,
)
CIN_YlGnBu = svariable(
    wrfname="cape_2d",
    ptitle="Max CIN (Convective Inhibition) [J/kg]",
    outfile="CIN_YlGnBu",
    range_min=0,
    range_max=1800,
    colormap=get_cmap("YlGnBu"),
)
CIN_YlGn = svariable(
    wrfname="cape_2d",
    ptitle="Max CIN (Convective Inhibition) [J/kg]",
    outfile="CIN_YlGn",
    scale="bounds",
    colormap=cmr.get_sub_cmap("YlGnBu", 0.0, 0.5, N=5),
    contour_color="darkgreen",
    contour_c_labels=False,
    bounds=[0, 10, 50, 100, 500, 1000],
    hide_edge_ticks=False,
    range_min=0,
    range_max=3000,
)
Rain = svariable(
    wrfname="RAINC",
    ptitle="Total Hourly Precipitation [mm]",
    outfile="Rain",
    windbarbs=1,
    isdif=1,
    ##################### Blues
    scale="linear",
    colormap=get_cmap("Blues"),
    range_min=0,
    range_max=60,
    nlevs=7,
    nticks=7,
    #####################
    ##################### Log
    # scale="log",
    # colormap=ListedColormap(
    #     [
    #         "white",
    #         "cyan",
    #         # "cornflowerblue",
    #         "blue",
    #         "darkgreen",
    #         "gold",
    #         "darkorange",
    #         "red",
    #         "magenta",
    #         "purple",
    #     ]
    # ),
    # nlevs=10,
    # logbase=2,
    # range_min=-3,
    # range_max=6,
    #####################
    ##################### Manunicast
    # scale="bounds",
    # colormap=ListedColormap(
    #     [
    #         "white",
    #         "cyan",
    #         "cornflowerblue",
    #         "blue",
    #         "lawngreen",
    #         "limegreen",
    #         "green",
    #         "darkgreen",
    #         "yellow",
    #         "gold",
    #         "darkorange",
    #         "red",
    #         "firebrick",
    #         "darkred",
    #         "magenta",
    #         "darkviolet",
    #         "bisque",
    #     ]
    # ),
    # bounds=[-0.1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    # range_min=0,
    # range_max=16,
    #####################
    ##################### Manuni-Log
    # scale="bounds",
    # colormap=ListedColormap(
    #     [
    #         "white",
    #         "cyan",
    #         "cornflowerblue",
    #         "blue",
    #         "lawngreen",
    #         "limegreen",
    #         # "green",
    #         "darkgreen",
    #         "yellow",
    #         "gold",
    #         "darkorange",
    #         "red",
    #         # "firebrick",
    #         "darkred",
    #         "magenta",
    #         "darkviolet",
    #         # "bisque",
    #     ]
    # ),
    # bounds=[-0.1, 0.5, 1, 2, 4, 6, 8, 10, 15, 20, 25, 30, 40, 50, 60],
    # range_min=0,
    # range_max=60,
    #####################
)
SimRadarReflectivityMax = svariable(
    wrfname="mdbz",
    ptitle="Maximum simulated radar reflectivity[dBZ]",
    outfile="SimRadarReflMax",
    windbarbs=1,
    scale="bounds",
    colormap=ListedColormap(
        [
            "white",
            "cyan",
            "deepskyblue",
            "blue",
            "steelblue",
            "lawngreen",
            "green",
            "gold",
            "darkorange",
            "red",
            "firebrick",
            "darkred",
            "indigo",
            "rebeccapurple",
            "mediumpurple",
            "lavender",
        ]
    ),
    bounds=[-0.1, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75],
    range_min=0,
    range_max=64,
)

# 3D + Field
AirTemp850 = svariable(
    dim=4,
    wrfname="temp",
    ptitle="Temperature at 850 hPa [K]",
    outfile="AirTemp850",
    nticks=12,
    nlevs=23,
    range_min=270,
    range_max=314,
    interpvar="pressure",
    interpvalue=850,
    colormap=get_cmap("Reds"),
)
AirTemp500 = svariable(
    dim=4,
    wrfname="temp",
    ptitle="Temperature at 500 hPa [K]",
    outfile="AirTemp500",
    nticks=9,
    nlevs=41,
    range_min=240,
    range_max=280,
    interpvar="pressure",
    interpvalue=500,
    colormap=get_cmap("Reds"),
    contour_color="maroon",
)
AirTempDif6h850 = svariable(
    dim=4,
    wrfname="temp",
    ptitle="Temperature change in 6h at 850 hPa [K]",
    outfile="AirTempDif6h850",
    range_min=-12,
    range_max=12,
    nticks=9,
    nlevs=9,
    interpvar="pressure",
    interpvalue=850,
    colormap=get_cmap("seismic"),
)
AirTempDif6h700 = svariable(
    dim=4,
    wrfname="temp",
    ptitle="Temperature change in 6h at 700 hPa [K]",
    outfile="AirTempDif6h700",
    range_min=-12,
    range_max=12,
    nticks=9,
    nlevs=9,
    interpvar="pressure",
    interpvalue=700,
    colormap=get_cmap("seismic"),
)
AirTempDif6h500 = svariable(
    dim=4,
    wrfname="temp",
    ptitle="Temperature change in 6h at 500 hPa [K]",
    outfile="AirTempDif6h500",
    range_min=-12,
    range_max=12,
    nticks=9,
    nlevs=9,
    interpvar="pressure",
    interpvalue=500,
    colormap=get_cmap("seismic"),
)
AirTempDif12h850 = svariable(
    dim=4,
    wrfname="temp",
    ptitle="Temperature change in 12h at 850 hPa [K]",
    outfile="AirTempDif12h850",
    range_min=-12,
    range_max=12,
    nticks=9,
    nlevs=9,
    interpvar="pressure",
    interpvalue=850,
    colormap=get_cmap("seismic"),
)
AirTempDif12h700 = svariable(
    dim=4,
    wrfname="temp",
    ptitle="Temperature change in 12h at 700 hPa [K]",
    outfile="AirTempDif12h700",
    range_min=-12,
    range_max=12,
    nticks=9,
    nlevs=9,
    interpvar="pressure",
    interpvalue=700,
    colormap=get_cmap("seismic"),
)
AirTempDif12h500 = svariable(
    dim=4,
    wrfname="temp",
    ptitle="Temperature change in 12h at 500 hPa [K]",
    outfile="AirTempDif12h500",
    range_min=-12,
    range_max=12,
    nticks=9,
    nlevs=9,
    interpvar="pressure",
    interpvalue=500,
    colormap=get_cmap("seismic"),
)
DewpointTemp850 = svariable(
    dim=4,
    wrfname="td",
    ptitle="Dewpoint Temperature at 850hPa [C]",
    outfile="DewpointTemp850",
    range_min=-75,
    range_max=25,
    interpvar="pressure",
    interpvalue=850,
    colormap=get_cmap("BuPu"),
)
RelativeHumidity700 = svariable(
    dim=4,
    wrfname="rh",
    ptitle="Relative Humidity at 700hPa [%]",
    outfile="RelHum700",
    range_min=0,
    range_max=100,
    interpvar="pressure",
    interpvalue=700,
    colormap=get_cmap("YlGnBu"),
)
PotentialTemp925 = svariable(
    dim=4,
    wrfname="theta",
    ptitle="Potential temperature at 925hPa [K]",
    outfile="PotTemp925",
    nticks=13,
    nlevs=25,
    range_min=270,
    range_max=330,
    interpvar="pressure",
    interpvalue=925,
    colormap=get_cmap("Reds"),
)
PotentialTemp850 = svariable(
    dim=4,
    wrfname="theta",
    ptitle="Potential temperature at 850hPa [K]",
    outfile="PotTemp850",
    nticks=11,
    nlevs=21,
    range_min=280,
    range_max=330,
    interpvar="pressure",
    interpvalue=850,
    colormap=get_cmap("Reds"),
)
PotentialTemp800 = svariable(
    dim=4,
    wrfname="theta",
    ptitle="Potential temperature at 800hPa [K]",
    outfile="PotTemp800",
    nticks=11,
    nlevs=21,
    range_min=280,
    range_max=330,
    interpvar="pressure",
    interpvalue=800,
    colormap=get_cmap("Reds"),
)
PotentialTemp700 = svariable(
    dim=4,
    wrfname="theta",
    ptitle="Potential temperature at 700hPa [K]",
    outfile="PotTemp700",
    nticks=11,
    nlevs=21,
    range_min=285,
    range_max=335,
    interpvar="pressure",
    interpvalue=700,
    colormap=get_cmap("Reds"),
)
PotentialTemp600 = svariable(
    dim=4,
    wrfname="theta",
    ptitle="Potential temperature at 600hPa [K]",
    outfile="PotTemp600",
    nticks=11,
    nlevs=21,
    range_min=285,
    range_max=335,
    interpvar="pressure",
    interpvalue=600,
    colormap=get_cmap("Reds"),
)
PotentialTemp500 = svariable(
    dim=4,
    wrfname="theta",
    ptitle="Potential temperature at 500hPa [K]",
    outfile="PotTemp500",
    nticks=11,
    nlevs=21,
    range_min=285,
    range_max=335,
    interpvar="pressure",
    interpvalue=500,
    colormap=get_cmap("Reds"),
)
GeoPotHeight500 = svariable(
    dim=4,
    ptitle="Geopotential Height at 500hPa [m]",
    outfile="GeoPotHeight500",
    nticks=13,
    nlevs=13,
    range_min=5340,
    range_max=6060,
    windbarbs=1,
    interpvar="pressure",
    interpvalue=500,
    colormap=get_cmap("Greens"),
    contour_color="darkslategray",
    contour_c_labels=False,
)
StaticStability700500 = svariable(
    dim=4,
    wrfname="temp",
    ptitle="Static stability at 700-500 hPa [C]",
    outfile="StaticStability700500",
    nticks=13,
    nlevs=25,
    range_min=6,
    range_max=30,
    interpvar="pressure",
    interpvalue=700,
    colormap=get_cmap("Oranges"),
)
StaticStability850700 = svariable(
    dim=4,
    wrfname="temp",
    ptitle="Static stability at 850-700 hPa [C]",
    outfile="StaticStability850700",
    nticks=14,
    nlevs=27,
    range_min=-4,
    range_max=22,
    interpvar="pressure",
    interpvalue=700,
    colormap=get_cmap("Oranges"),
    contour_color="maroon",
)
SimRadarReflectivity1km = svariable(
    dim=4,
    wrfname="dbz",
    ptitle="Simulated radar reflectivity at 1km [dBZ]",
    outfile="SimRadarRefl1km",
    interpvar="z",
    interpvalue=1000,
    windbarbs=1,
    scale="bounds",
    colormap=ListedColormap(
        [
            "white",
            "cyan",
            "deepskyblue",
            "blue",
            "steelblue",
            "lawngreen",
            "green",
            "gold",
            "darkorange",
            "red",
            "firebrick",
            "darkred",
            "indigo",
            "rebeccapurple",
            "mediumpurple",
            "lavender",
        ]
    ),
    bounds=[-0.1, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75],
    range_min=0,
    range_max=64,
)
Frontogenesis925 = svariable(
    dim=4,
    ptitle="Petterssen Frontogenesis at 925 hPa [K/(100km 3h)]",
    outfile="Frontogenesis925",
    overlap_sv="PotentialTemp925",
    overlap_gap=1,
    overlap_cmap=get_cmap("coolwarm"),
    windbarbs=1,
    interpvar="pressure",
    interpvalue=925,
    scale="bounds",
    bounds=[-16, -8, -4, -2, -1, -0.5, 0.5, 1, 2, 4, 8, 16],
    colormap=ListedColormap(
        [
            "midnightblue",
            "darkblue",
            "blue",
            "deepskyblue",
            "cyan",
            "white",
            "yellow",
            "darkorange",
            "red",
            "firebrick",
            "darkred",
        ]
    ),
    range_min=-8,
    range_max=8,
)
Frontogenesis850 = svariable(
    dim=4,
    ptitle="Petterssen Frontogenesis at 850 hPa [K/(100km 3h)]",
    outfile="Frontogenesis850",
    overlap_sv="PotentialTemp850",
    overlap_gap=1,
    overlap_cmap=get_cmap("coolwarm"),
    windbarbs=1,
    interpvar="pressure",
    interpvalue=850,
    scale="bounds",
    bounds=[-16, -8, -4, -2, -1, -0.5, 0.5, 1, 2, 4, 8, 16],
    colormap=ListedColormap(
        [
            "midnightblue",
            "darkblue",
            "blue",
            "deepskyblue",
            "cyan",
            "white",
            "yellow",
            "darkorange",
            "red",
            "firebrick",
            "darkred",
        ]
    ),
    range_min=-8,
    range_max=8,
)
Frontogenesis700 = svariable(
    dim=4,
    ptitle="Petterssen Frontogenesis at 700 hPa [K/(100km 3h)]",
    outfile="Frontogenesis700",
    overlap_sv="PotentialTemp700",
    overlap_gap=1,
    overlap_cmap=get_cmap("coolwarm"),
    windbarbs=1,
    interpvar="pressure",
    interpvalue=700,
    scale="bounds",
    bounds=[-16, -8, -4, -2, -1, -0.5, 0.5, 1, 2, 4, 8, 16],
    colormap=ListedColormap(
        [
            "midnightblue",
            "darkblue",
            "blue",
            "deepskyblue",
            "cyan",
            "white",
            "yellow",
            "darkorange",
            "red",
            "firebrick",
            "darkred",
        ]
    ),
    range_min=-8,
    range_max=8,
)
Frontogenesis500 = svariable(
    dim=4,
    ptitle="Petterssen Frontogenesis at 500 hPa [K/(100km 3h)]",
    outfile="Frontogenesis500",
    overlap_sv="PotentialTemp500",
    overlap_gap=1,
    overlap_cmap=get_cmap("coolwarm"),
    windbarbs=1,
    interpvar="pressure",
    interpvalue=500,
    scale="bounds",
    bounds=[-16, -8, -4, -2, -1, -0.5, 0.5, 1, 2, 4, 8, 16],
    colormap=ListedColormap(
        [
            "midnightblue",
            "darkblue",
            "blue",
            "deepskyblue",
            "cyan",
            "white",
            "yellow",
            "darkorange",
            "red",
            "firebrick",
            "darkred",
        ]
    ),
    range_min=-8,
    range_max=8,
)

# SkewT
# https://www.umr-cnrm.fr/dbfastex/datasets/rsc_data.html
SkewT = svariable(
    ptitle="SkewT at 53.3638,-2.2764",  # WMO_code  Alt[m]
    outfile="SkewT",
    windbarbs=1,
    lat=53.3638,
    lon=-2.2764,
    range_min=-60,
    range_max=40,
)
SkewT_Casablanca = svariable(
    ptitle="SkewT at 33.57,-7.67 (MOROCCO Casablanca)",  # 60155    56
    outfile="SkewT_Gibraltar",
    windbarbs=1,
    lat=33.57,
    lon=-7.67,
    range_min=-60,
    range_max=40,
)
SkewT_Algeria = svariable(
    ptitle="SkewT at 31.62,-2.23 (ALGERIA Bechar)",  # 60571  81
    outfile="SkewT_Algeria",
    windbarbs=1,
    lat=31.62,
    lon=-2.23,
    range_min=-60,
    range_max=40,
)
SkewT_Lerwick = svariable(
    ptitle="SkewT at 60.13,-1.18 (UK Lerwick)",  # 03005  82
    outfile="SkewT_Lerwick",
    windbarbs=1,
    lat=60.13,
    lon=-1.18,
    range_min=-60,
    range_max=40,
)
SkewT_Stornoway = svariable(
    ptitle="SkewT at 58.22,-6.32 (UK Stornoway)",  # 03026  9
    outfile="SkewT_Stornoway",
    windbarbs=1,
    lat=58.22,
    lon=-6.32,
    range_min=-60,
    range_max=40,
)
SkewT_Nottingham = svariable(
    ptitle="SkewT at 53.00,-1.25 (UK Nottingham)",  # 03354  117
    outfile="SkewT_Nottingham",
    windbarbs=1,
    lat=53.00,
    lon=-1.25,
    range_min=-60,
    range_max=40,
)
SkewT_Aberporth = svariable(
    ptitle="SkewT at 52.13,-4.57 (UK Aberporth)",  # 03502  133
    outfile="SkewT_Aberporth",
    windbarbs=1,
    lat=52.13,
    lon=-4.57,
    range_min=-60,
    range_max=40,
)
SkewT_Larkhill = svariable(
    ptitle="SkewT at 51.20,-1.80 (UK Larkhill)",  # 03743  132
    outfile="SkewT_Larkhill",
    windbarbs=1,
    lat=51.20,
    lon=-1.80,
    range_min=-60,
    range_max=40,
)
SkewT_Camborne = svariable(
    ptitle="SkewT at 50.22,-5.32 (UK Camborne)",  # 03808  88
    outfile="SkewT_Camborne",
    windbarbs=1,
    lat=50.22,
    lon=-5.32,
    range_min=-60,
    range_max=40,
)
SkewT_Herstmonceux = svariable(
    ptitle="SkewT at 50.90,0.32 (UK Herstmonceux)",  # 03882  52
    outfile="SkewT_Herstmonceux",
    windbarbs=1,
    lat=50.90,
    lon=0.32,
    range_min=-60,
    range_max=40,
)
SkewT_Trappes = svariable(
    ptitle="SkewT at 48.77,2.02 (FRANCE Trappes)",  # 07145  168
    outfile="SkewT_Trappes",
    windbarbs=1,
    lat=48.77,
    lon=2.02,
    range_min=-60,
    range_max=40,
)
SkewT_Bordeaux = svariable(
    ptitle="SkewT at 44.82,-0.68 (FRANCE Bordeaux)",  # 07510 48
    outfile="SkewT_Bordeaux",
    windbarbs=1,
    lat=44.82,
    lon=-0.68,
    range_min=-60,
    range_max=40,
)
SkewT_Nimes = svariable(
    ptitle="SkewT at 43.87,4.40 (FRANCE Nimes)",  # 07645  60
    outfile="SkewT_Nimes",
    windbarbs=1,
    lat=43.87,
    lon=4.40,
    range_min=-60,
    range_max=40,
)
SkewT_LaCoruna = svariable(
    ptitle="SkewT at 43.37,-8.42 (SPAIN La Coruna)",  # 08001  58
    outfile="SkewT_LaCoruna",
    windbarbs=1,
    lat=43.37,
    lon=-8.42,
    range_min=-60,
    range_max=40,
)
SkewT_Santander = svariable(
    ptitle="SkewT at 43.47,-3.82 (SPAIN Santander)",  # 08023  64
    outfile="SkewT_Santander",
    windbarbs=1,
    lat=43.47,
    lon=-3.82,
    range_min=-60,
    range_max=40,
)
SkewT_Madrid = svariable(
    ptitle="SkewT at 40.45,-3.55 (SPAIN Madrid)",  # 08221  633
    outfile="SkewT_Madrid",
    windbarbs=1,
    lat=40.45,
    lon=-3.55,
    range_min=-60,
    range_max=40,
)
SkewT_Murcia = svariable(
    ptitle="SkewT at 38.00,-1.17 (SPAIN Murcia)",  # 08430  62
    outfile="SkewT_Murcia",
    windbarbs=1,
    lat=38.00,
    lon=-1.17,
    range_min=-60,
    range_max=40,
)
SkewT_Gibraltar = svariable(
    ptitle="SkewT at 36.15,-5.35 (GIBRALTAR Gibraltar)",  # 08495  3
    outfile="SkewT_Gibraltar",
    windbarbs=1,
    lat=36.15,
    lon=-5.35,
    range_min=-60,
    range_max=40,
)
