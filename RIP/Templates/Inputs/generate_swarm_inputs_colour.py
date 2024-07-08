import sys


if len(sys.argv) != 14:
    usage_message = """
    Usage: generate_swarm_inputs.py file_path x0 x1 xn y0 y1 yn p t0 tf tdt fdt hydrometeor

    Generates a list of x, y and p coordinates for a swarm of particles.

    For example, to generates 100 particles in a 3x3 grid between (0, 0) and (1, 2) at 850hPa:
        python generate_swarm_inputs.py 0 1 3 0 4 5 850

    The output is a swarm.inputs file to be used to generate a plot directly, in the form:
    #traj_t_0   traj_t_f    traj_dt     file_dt    traj_x         traj_y       traj_p   hydrometeor     colour
    $t0         $tf         $tdt        $fdt       $all_traj_x    $traj_y_1    $traj_p  $hydrometeor    violet
    $t0         $tf         $tdt        $fdt       $all_traj_x    $traj_y_2    $traj_p  $hydrometeor    magenta
    $t0         $tf         $tdt        $fdt       $all_traj_x    $traj_y_3    $traj_p  $hydrometeor    red
    ...

    Where the colours are the presets: violet, magenta, red, orange, mustard, green, dark.green, blue, light.blue, and cyan.

    In the example above, the output would be:
    #traj_t_0   traj_t_f   traj_dt   file_dt   traj_x    traj_y   traj_p        hydrometeor   colour
    0           1          1         1         0,0.5,1   0,0,0    850,850,850   0             violet
    0           1          1         1         0,0.5,1   1,1,1    850,850,850   0             magenta
    0           1          1         1         0,0.5,1   2,2,2    850,850,850   0             red
    0           1          1         1         0,0.5,1   3,3,3    850,850,850   0             orange
    0           1          1         1         0,0.5,1   4,4,4    850,850,850   0             mustard
    """

    print(usage_message)
    sys.exit(1)

f = sys.argv[1]
x0 = float(sys.argv[2])
x1 = float(sys.argv[3])
xn = int(sys.argv[4])
y0 = float(sys.argv[5])
y1 = float(sys.argv[6])
yn = int(sys.argv[7])
p = int(sys.argv[8])
t0 = int(sys.argv[9])
tf = int(sys.argv[10])
tdt = int(sys.argv[11])
fdt = int(sys.argv[12])
hydrometeor = int(sys.argv[13])

colours = [
    "cyan",
    "light.blue",
    "blue",
    "dark.green",
    "green",
    "mustard",
    "orange",
    "red",
    "magenta",
    "violet",
]
x = [x0 + i * (x1 - x0) / (xn - 1) for i in range(xn)]
y = [y1 - i * (y1 - y0) / (yn - 1) for i in range(yn)]
p = [p] * len(x)

all_x = ",".join(f"{xi:.2f}" for xi in x)
all_p = ",".join(map(str, p))
# Spaces Padding
xspace = " " * (len(all_x) - 5)
pspace = " " * (len(all_p) - 5)

if len(y) > len(colours):
    # Cycle over colours vector
    colours = colours * (len(y) // len(colours) + 1)


with open(f, "w") as f:
    f.write(
        f"#traj_t_0   traj_t_f   traj_dt   file_dt   traj_x {xspace} traj_y {xspace} traj_p {pspace} hydrometeor   colour\n"
    )
    for y_i in y:
        this_y = [y_i] * len(x)
        all_y = ",".join(f"{y:.2f}" for y in this_y)
        yspace = " " * (len(all_y) - 5)
        this_colour = colours.pop(0)
        f.write(
            f"{t0}           {tf}          {tdt}       {fdt}      {all_x}   {all_y}   {all_p}   {hydrometeor}             {this_colour}\n"
        )
