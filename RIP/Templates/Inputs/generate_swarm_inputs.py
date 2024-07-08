import sys


if len(sys.argv) != 8:
    usage_message = """
    Usage: generate_swarm_inputs.py x0 x1 xn y0 y1 yn p

    Generates a list of x, y and p coordinates for a swarm of particles.

    For example, to generates 100 particles in a 3x3 grid between (0, 0) and (1, 2) at 850hPa:
        python generate_swarm_inputs.py 0 1 3 0 2 3 850

    The output is a coma-separated string of x values, followed by a space,
    followed by a coma-separated string of y values, and then p values.
    In the example above, the output would be:
        0,0.5,1,0,0.5,1,0,0.5,1 2,2,2,1,1,1,0,0,0 850,850,850,850,850,850,850,850,850
    """

    print(usage_message)
    sys.exit(1)

x0 = float(sys.argv[1])
x1 = float(sys.argv[2])
xn = int(sys.argv[3])
y0 = float(sys.argv[4])
y1 = float(sys.argv[5])
yn = int(sys.argv[6])
p = int(sys.argv[7])

x = [x0 + i * (x1 - x0) / (xn - 1) for i in range(xn)]
y = [y1 - i * (y1 - y0) / (yn - 1) for i in range(yn)]

all_x = []
all_y = []
all_p = []
for y_i in y:
    all_x.extend(x)
    # repeat current y value xn times
    all_y.extend([y_i] * len(x))
    # repeat p xn times
    all_p.extend([p] * len(x))
assert len(all_x) == len(all_y)
assert len(all_x) == len(all_p)
print(
    f"{','.join(map(str, all_x))} {','.join(map(str, all_y))} {','.join(map(str, all_p))}"
)
