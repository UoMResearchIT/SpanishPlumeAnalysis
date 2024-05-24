import os
import sys

cwd = os.path.dirname(os.path.abspath(__file__))

diags = {
    "xlat": "Latitude [deg]",
    "xlon": "Longitude [deg]",
    "ter": "Elevation [m]",
    "prs": "Pressure [mb]",
    "ght": "Geopotential Height [m]",
    "ghtagl": "Geopotential Height Above Ground Level [m]",
}

g1 = {
    "tmc": "Air Temperature [C]",
    "the": "Potential Temperature [K]",
    "eth": "Equivalent Potential Temperature [K]",
    "tdp": "Dewpoint Temperature [C]",
    "rhu": "Relative Humidity [%]",
    "qvp": "Water Vapor Mixing Ratio [g/kg]",
    "lcl": "Lifted Condensation Level [m]",
    "lfc": "Level of Free Convection [m]",
    "omg": "Omega [mb/s]",
    "pvm": "Moist Potential Vorticity",
    "pvo": "Potential Vorticity",
    "wsp": "Wind Speed [m/s]",
    "wdr": "Horizontal Wind Direction [deg]",
    "www": "Vertical velocity [cm/s]",
}
g2 = {
    "sateth": "Saturated Equivalent Potential Temperature [K]",
    "stb": "Static Stability [K/hPa]",
    "stbe": "Equivalent Static Stability [K/hPa]",
    "stbz": "Buoyancy [K/km]",
    "tdd": "Temperature Deficit [C]",
    "cin3": "Convective Inhibition [J/kg]",
    "cap3": "Convective Available Potential Energy [J/kg]",
    "mcap": "Most Unstable Convective Available Potential Energy [J/kg]",
    "mcin": "Most Unstable Convective Inhibition [J/kg]",
}

if len(sys.argv) == 2:
    if sys.argv[1] == "none":
        diags = {
            "xlat": "Latitude [deg]",
            "xlon": "Longitude [deg]",
        }
    elif sys.argv[1] == "g1":
        diags = {**diags, **g1}
    elif sys.argv[1] == "g2":
        diags = {**diags, **g2}
    else:
        print("Invalid argument. Use 'none', 'g1', 'g2', or no argument.")
        sys.exit(1)

# Generate traj.template
template = """&userin
 itrajcalc=1
 /
 &trajcalc
 rtim=$traj_t_0,ctim=$traj_t_f,dtfile=$file_dt.,dttraj=$traj_dt.,vctraj='p',
 xjtraj=$traj_x,
 yitraj=$traj_y,
 zktraj=$traj_z,
 ihydrometeor=$hydrometeor
 /
===========================================================================
----------------------    Plot Specification Table    ---------------------
===========================================================================
"""
header = "Time [h],"
for diag, label in diags.items():
    template += f"feld={diag}\n"
    template += (
        f"===========================================================================\n"
    )
    header += f"{label},"
header = header[:-1]
with open(f"{cwd}/traj.template", "w") as f:
    f.write(template)

# Generate tabdiag_format.template
with open(f"{cwd}/tabdiag_format.template", "w") as f:
    f.write(f"'{header}'\n")
    f.write(f"'({len(diags)+1}(3x,f9.3,3x))'\n")
