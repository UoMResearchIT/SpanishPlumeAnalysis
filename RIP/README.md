# About the scripts

The scripts in this folder make use of a RIP singularity container to produce backward trajectories.
There are mainly two ways to interact with the container in these scripts.

The `singularity_rip.sh` script directly invokes the container, and processes a single trajectory, so it is mostly meant for testing.
The `CSF/Submit.sh` script is for submitting jobs to the csf, so it eventually calls `singularity_rip.sh` in each job.

There are mainly two steps in the process: RIPDP pre-processing, and trajectory computation.

## RIPDP pre-processing

This step only needs to be performed once per set of wrf data, and can be reused to compute many trajectories a posteriori.

For this step, we need to provide the wrf data with the flag `--wrfdata` (or `-wd`), and an output directory (with `--outputdir` or `-od`). For example:
```
./singularity_rip.sh --wrfdata="/my/wrfout/files/dir" --outputdir="/my/output/dir" -nt -np
```
This creates the output directory and, inside it, a `RIPDP` directory, where it saves all the preprocessing outputs.

The `-nt -np` flags are to skip trajectory computation and plot generation steps, so it will only perform the preprocessing step.

Important settings for the pre-processing include the simulation time-step, and the desired range of times that you want to pre-process.
This can be set with the flags `dt`, `t_0` and `t_f`, respectively (they default to 1, 0 and 168).
For example, this pre-processes the first 6 hours:
```
./singularity_rip.sh -od="/my/output/dir" -wd="/my/wrfout/files/dir" -nt -np --dt=1 --t_0=0 --t_f=5
```

#### Details you need not worry about unless you are debugging something

Internally, the script will first create an rdp_rip file from the `./Templates/rdp.template`, and save it in `/my/output/dir/RIPDP`.
Then, it will create a `run_rdp.sh` file in the outputs directory.
This script is then executed inside the container, and generates a bunch of `rdp_rip_*` files in the `RIPDP` directory.

## Trajectory computation and plotting

Once the wrfout files have been pre-processed, we can basically forget about them and only look at the ripdp outputs to generate the trajectories.

A run to compute backward trajectories from the pre-processed data we already generated would look like this:
```
./singularity_rip.sh -od="/my/output/dir" --noRDP --trajtimes=5-3 --trajplot="MyPlot"
```
This will produce a plot `MyPlot.pdf` in `/my/output/dir` with the trajectories.

The `noRDP` flag is there to skip the pre-processing step, which we had already done.

Note that we are using the same output directory as in the pre-processing step.
The script will try to find the `RIPDP` directory in there.

The `trajtimes` parameter specifies the times for which we want to plot a trajectory, and is specified with two numbers separated by a `-`.
 - The first number represents the "begining" of the trajectory (`traj_t_0`), that is, the time in which the particles at the specified locations will begin to be tracked, or "release time" (rtim) in rip terms.
 - The second number represents the "end" of the trajectory (`traj_t_f`), taht is, the time in which tracking stops, or completion time (ctim) in rip terms.
If the release time is larger than the completion time, a **backward trajectory** is calculated. If the reverse is true, a **forward trajectory** is calculated.

The `trajplot` parameter specifies the name of the trajectory plot, and it defaults to use `trajtimes` prepended with "tp_".

There are a few more things that can be tweaked for the trajectories.
 - The location of the released particles can be set with `traj_x` and `traj_y`.
 - The time step of the numerical computation of the trajectory can be set with `traj_dt`. This is measured in seconds, not hours.
 - The time step of the pre-processed ripdp files can be changed with `file_dt`. This is also measured in seconds.

### Trajectory inputs file

By default, the values provided for the parameters above will be replaced in a template file (`./Templates/traj_inputs.template`), producing a `.inputs` file.
The template is currently set to compute trajectories at different pressure levels (from 600 to 850, every 50 hPa).
This file also specifies the colours of the lines (you can see all available colours in `Templates/color.tbl`).

Alternatively, you can produce the .inputs file independently, and pass it with the parameter `trajinputs`.
For example, you can have a file called `my_traj_inputs_file` with this contents:
```
#traj_t_0 traj_t_f traj_dt file_dt traj_x traj_y traj_p hydrometeor color
5         2        600     3600    190    400    900    0           red
1         4        600     3600    100    250    750    0           blue
```
and run
```
./singularity_rip.sh -od="/my/output/dir" --noRDP --trajinputs="my_traj_inputs_file" --trajplot="tp_my_inputs"
```
Note that since all the trajectory parameters need to be already specified in the inputs file, we should only pass the plot name with `trajplot`.


#### Details you need not worry about unless you are debugging something

Internally, the script will copy the trajectory inputs file, reformat it, and save it in `/my/output/dir/BTrajectories` as `*_traj_inputs`.

Then it  create a trajectory specification file for each line in the trajectory inputs file, using the `./Templates/traj.template`, and save them in the same directory as `*_traj_x.in`.

Then it will create a `/my/output/dir/run_MyPlot_traj_i.sh` from the `./Templates/run.template`, which is executed inside the container to generate the trajectories.
This script is then executed multiple times inside the container (the file is actually modified as it iterates trhough the trajectories, so in the end you will only see one file. Inside it, you should see the `_traj_x.in` with the number of the last trajectory calculated).

This generates a bunch of `.out`, `.traj` and `.diag` files in the `BTrajectories` directory, that will get used for the plotting.

You can inspect things at this point if you use the `-np` flag, which skips the plot generation.


### Plot specification file

Once the trajectory is calculated, it needs to be plotted.
Configuring the plots in rip is no easy feat.

If you wish to configure the plot... I can only wish you good luck and refer you to [the docs](https://a.atmos.washington.edu/~ovens/ripug_uw.html#traj).
Well, no, I can do better. See the description of the options being used below.

As for understanding the steps in the script:

The script assumes a standard plot format that is recorded in the `./Templates/traj_plot.template`.
The parameters for the template come from the `Trajectory_Spec_List`, inside the `singularity_rip.sh` script.

That template turns into a `.in` file in the outputs directory (in the example above, `/my/output/dir/MyPlot.in`).

The script will also create a `/my/output/dir/run_MyPlot.sh` file from the `./Templates/run.template`.
This script is then executed inside the container to generate the plot using `MyPlot.in`.

#### Options being used:
- `feld`: Field to be plotted
    Set to `arrow`, the size of arrow head represents the height of the trajectory.
    Set to `map` for the background map, and to `tic` for the box with grid numbers.
- `ptyp`: Plot type
    Set to `ht`, which means a horizontal (map view) trajectory plot.
    Set to `hb` for the background images of the map and ticks.
- `tjfl`: File name of trajectory position info.
    Set to the relevant `.traj` file.
- `vcor`: Vertical coordinate
    Set to `s`, which means pressure.
- `colr`: Plot color
    Choose from the `color.tbl`.
- `nmsg`: No message
    Prevents legend for arrow sizes.
- `tjst`: Start time (in forecast hour) of plotted trajectories.
    This has to be between `traj_t_0` and `traj_t_f`, and smaller than `tjen`.
    It is set to the min trajectory time.
- `tjen`: End time (in forecast hour) of plotted trajectories.
    This has to be between `traj_t_0` and `traj_t_f`, and larger than `tjst`.
    It is set to the max trajectory time.
- `titl`: Plot title
    Specifies the trajectory title (legend). Use underscore (`_`) instead of space.
- `axlg`: Large labeled tick increment for horizontal plots.
    Set to 50. Specifies the horizontal tick interval.

#### Other potentially useful options:
- `nttl`: No plot title
    Removes the trajectory title (legend).

# System requirements

You need to have a working installation of singularity (aptainer) for the scripts to work, and the ripdocker_latest.sif image.

To install apptainer see the [apptainer docs](https://apptainer.org/docs/admin/main/installation.html#install-ubuntu-packages).

Once you have a working copy of apptainer, you can pull the image with
```
apptainer pull docker://fcoherreazcue/ripdocker:latest
```
This should create a ripdocker_latest.sif file.

You also need to have access to some `wrfout` files, to pre-process with ripdp, or the preprocessed files.

You are now set to start using the scripts.

