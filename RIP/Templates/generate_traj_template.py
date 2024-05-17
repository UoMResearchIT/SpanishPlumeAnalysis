import os

cwd = os.path.dirname(os.path.abspath(__file__))

diags = {
    "xlat": "Latitude [deg]",
    "xlon": "Longitude [deg]",
    "ter": "Elevation [m]",
    "prs": "Pressure [mb]",
    "tmk": "Air Temperature [K]",
    "the": "Potential Temperature [K]",
    "eth": "Equivalent Potential Temperature [K]",
    "tdk": "Dewpoint Temperature [K]",
    "rhu": "Relative Humidity [%]",
}

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
