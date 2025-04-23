# Generating new diagnostics

The workflow to generate new results involves using the csf.

## Submitting jobs to csf

If this is the first time you are using the csf, you will need to:

<details>
<summary>Get the code.</summary>

- Move to a node with internet connection with
    ```
    qrsh -l short
    ```

- Make sure you have git installed and that you are signed in to your github account.
    <details>
    <summary>How do I set up git?</summary>

    </details>

- Clone the repository with:

    ```
    git clone git@github.com:UoMResearchIT/SpanishPlumeAnalysis.git SpanishPlumeAnalysis
    cd SpanishPlumeAnalysis
    ```

</details>

<details>
<summary>Set up your conda environment.</summary>

- See [conda environment](#conda-environment) for instructions on how to set up the conda environment.

</details>

<details>
<summary>Get the RIP container image.</summary>

If you want to be able to generate diagnostics using RIP, you need the container to run them.
Since the CSF only allows apptainer (singularity) and not docker, you need to convert the image.

- Pull the container image with
  ```
  apptainer pull docker://fcoherreazcue/ripdocker:latest
  ```
- Move the image to the `RIP` folder with
  ```
  mv ripdocker_latest.sif RIP/ripdocker_latest.sif
  ```

</details>

<details>
<summary>Set up the result packaging and uploading utilities.</summary>

- See the [packaging results and uploading to dropbox](#packaging-results-and-uploading-to-dropbox) section for instructions on how to do this.

</details>

All the commands below work if you are in the base folder that you cloned, i.e. `.../SpanishPlumeAnalysis`.

If you want to follow the examples, create a folder to save the results with `mkdir Diagnostics`.

### WRF diagnostics

The `CSF/Submit.sh` is a bash script that does most of the heavy lifting.


To use it, you need a file with the inputs, e.g. `Diagnostics/test.inputs`, that looks something like this:

```
--task=diagnostic --var=SeaLevelPressure --dir_path=/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/ --outdir=Test_SLP/
--task=diagnostic --var=DewpointTemp2m   --dir_path=/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/ --save_pdf_frames=1 --outdir=Test_DewpTemp/
```

**Note** The inputs file is a list of the arguments passed to the `csf.py` script, one per line.
You can find some sample files in the `CSF` directory. The program being called (`csf.py`) has to be omitted.

Now you can submit the jobs with:

```
./CSF/Submit.sh Diagnostics/test.inputs Diagnostics/TestWRF
```

The script will create a jobarray and submit each line in the `.inputs` file.
It will also make sure that the `outdir` directories exist (or it will create them) in `Diagnostics/TestWRF` to save the results.

### RIP diagnostics

Generating diagnostics for RIP can be a bit confusing, so it is best that you look at the dedicated [readme](RIP/README.md), but a quick reference is provided here for convenience.

In a similar way, the `CSF/SubmitRIP.sh` does most of the heavy lifting.

To use it, you need a file with the inputs, e.g. `Diagnostics/test_rip.inputs`, that looks something like this:

```
-tt=110-90 --traj_x=412 --traj_y=195 -tp=Test_RIP_CSF_back -pd=/mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/RIP/Results/RIPDP/Control/rdp_Control -od=Test_RIP_CSF_back
-tt=90-110 --traj_x=412 --traj_y=195 -tp=Test_RIP_CSF_forward -pd=/mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/RIP/Results/RIPDP/Control/rdp_Control -od=Test_RIP_CSF_forward
```

**Note** The inputs file is a list of the arguments passed to the `singularity_rip.sh` script, one per line. You can find some sample files in the `RIP/CSF` directory. The program being called (`singularity_rip.sh`) has to be omitted.


Now you can submit the jobs with:

```
RIP/CSF/Submit.sh Diagnostics/test_rip.inputs Diagnostics/TestRIP
```

The script will create a jobarray and submit each line in the `.inputs` file.
It will also make sure that the `od` directories exist (or it will create them) in `Diagnostics/TestRIP` to save the results.


## Packaging results and uploading to dropbox

The repo has a few utility scripts to help you package the results and upload them to dropbox.

To be able to use them, you need to copy the scripts to ~/bin, and make them executable:
```
cp utilities/dbxcli-r.sh ~/bin/
cp utilities/zip_pdf_frames.sh ~/bin/zip-frames.sh
cp utilities/zip_traj_files.sh ~/bin/zip-traj-files.sh
chmod +x ~/bin/dbxcli-r.sh
chmod +x ~/bin/zip-frames.sh
chmod +x ~/bin/zip-traj-files.sh
```
You will also need to install the `dbxcli` package, which can be found [here](https://github.com/dropbox/dbxcli).

### zip_pdf_frames

This script looks for all the pdf files that were generated for the animations, and zips them into a single file. It is important to run this script before uploading to dropbox, so that they are not uploaded as individual files.
This is particularly important when the save_pdf_frames flag is set to 1.
You can run it with:
```
zip-frames <dir>
```
for example:
```
zip-frames ./Diagnostics/TestWRF/Test_DewpTemp/
```

### zip_traj_files

This script looks for all the files that are not csv or pdf files recursively, and zips them into a single file. Since the pdf and csv files are usually the only files you want as ouputs from a RIP diagnostic, this is a good way to package the results.
You can run it with:
```
zip_traj_files <dir>
```
for example:
```
zip-traj-files Diagnostics/TestRIP/Test_RIP_CSF_forward/
```
or even at a higher level:
```
zip-traj-files Diagnostics/TestRIP/
```

### dbxcli-r

This is a wrapper for the `dbxcli` command, which allows you to upload files recursively to dropbox.
Once you have it set up, you can use it with:
```
dbxcli-r put <source> <destination> [--dry-run]
```
for example:
```
dbxcli-r put "./Diagnostics/TestRIP" "/Spanish Plume/testDiagnostics/TestRIP" --dry-run
```
The `--dry-run` flag makes it so that it does not actually push anything to dropbox, but tells you what it would do.
If you are sure you want to go ahead and push to dropbox, remove the `--dry-run` flag and run it again.


## File transfer

If you prefer to transfer files directly, skipping dropbox, you can do so.

Transfering files to and from the csf is simpler if using sshfs,
which mounts a folder from the csf to your computer.
So, create an empty folder to host the contents from the CSF:
```
mkdir sshfs_to_csf
```
Then, use sshfs as sshfs `user@dest:/path/to/folder local/path`,
```
sshfs mbcxpfh2@csf3.itservices.manchester.ac.uk:/mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis sshfs_to_csf/
```
You should see everything in that folder, and so copy to and from that folder.


# About the scripts

## csf
This script parses the arguments from the command line, and is able to generate a WRF diagnostic from a single line of code.
The main arguments to use include:

**task**, which can be *diagnostic*, *wrfcompare*, *mp4diff* or *mp4stitch*.
**var**, which can be any of the predefined **SensibleVariables**.
**dirs**, which is the directory (or directories) of the source files.
**files**, which is the list of names of files, when being compared.
**labels**, which is the list of labels added when files are being compared or stitched.
**outdir**, which is the directory where outputs will be saved.

The following are sample calls for this function:

*python csf.py --task=diagnostic --var=Rain --dir_path=./MyData/ --outdir=./*

*python csf.py --task=wrfcompare --var=SeaLevelPressure --dirs="Data1,Data2" --outdir=./ --difflabel=Data2-Data1*

*python csf.py --task=mp4diff --var=DewpointTemp850 --dirs="./MP4_1,./MP4_2/" --labels="MP4_1,MP4_2,MP4Diff"*

*python csf.py --task=mp4stitch --dirs="MyVideos" --files="f1,f2,f3,f4" --N=2 --M=2*

### Diagnostic computation time
| ***svariable***       | min |
| --------------------- | --- |
| DewpointTemp2m        | 19  |
| AirTemp2m             | 20  |
| DewpointTemp850       | 26  |
| AirTemp850            | 28  |
| StaticStability700500 | 28  |
| StaticStability850700 | 28  |
| GeoPotHeight500       | 30  |
| SeaLevelPressure      | 30  |
| Rain                  | 44  |
| RelHum2m              | 44  |
| RelHum700             | 44  |
| CIN                   | 45  |
| SimRadarRefl1km       | 76  |
| SimRadarReflMax       | 98  |
| CAPE                  | 99  |

## Animate
This is the core of the diagnostic generation.
In this function all your wrfout files are loaded, the variables are extracted using **GetSensVar**, plotted using **Plot2DField**, and combined into an mp4.

*All* the files in ***dir_path*** will be loaded and combined, so make sure you want that.

The information on the diagnostic being generated should be provided in an ***svariable*** object, as defined in **SensibleVariables**.

Should you wish to override the default windbarb overlapping defined for some **SensibleVariables**, the call to this function is the best place to do so.

By default, when the animation is processed and the mp4 is successfully generated all png files are deleted. This can be controled with the flag ***cleanpng***.

## Plot2DField
This function simply plots a given variable (***var***) with the metadata found in the ***svariable*** object.

A flag for ***windbarbs*** may be turned on, for which the wind components ***u*** and ***v*** must be given as inputs too.

## SensibleVariables
This defines a class for variables with more sensible names than the ones used in wrf, which makes it a bit more amicable.

The object is basically composed of metadata for the diagnostics that are of interest to this particular project, but the list can easily be expanded.

The information in each object is used as instructions in the extraction of the variable from netcdf files and during plotting.

Each of the variables has the attributes that describe the way the variable should be plotted, including the colour scale, units, title, range, type of plot, annotations (like wind-barbs or contour-lines), and potentially overlapping variables.

See the description of each predefined **svariable** inside the file.

## GetSensVar
This function is an adaptation of wrf-python's *getvar*, but makes it simpler to obtain the diagnostics of interest, and uses the information in **svariable** objects

It deals with all the tecnical details on how to load the variables from the netcdf file so that they can be passed to the **Plot2DField** function.
This includes loading the wind velocity components when ***windbarbs*** is set to 1.

During this process, it also takes care of some variable computation, which is not universally implemented in *getvar*.

The outputs are the processed variable ***var***, the wind velocity components ***u*** and ***v*** (if windbarbs=0 these will be None), and the raw variable values ***varv*** (for use in *isdif* **svariable** computation).


## Special diagnostics

The following diagnostics have special functions to deal with them, but the diagnostic generation is still done through the csf script.

### TerrainPlots
These do not require animation nor the whole of the wrfout files, so they have a special function to deal with them.
They use the same **Plot2DField** function, and add annotations to the plot.

### Frontogenesis
This is a special diagnostic that requires a bit of extra computation. The function is called from within GetSensVar, and passed to Animate as the other diagnostics.

### SkewT
SkewTs are a completely different plotting style, and so they have a special function to deal with them,
which uses the [metpy](https://unidata.github.io/MetPy/latest/api/index.html) library.
They also combine a lot of wrf variables, so they are not generated in the same way as the other diagnostics.
The function is called from Animate, as an alternative to the standard Plot2DField for other diagnostics.


## Direct comparison of outputs

The `MP4Compare` and `WRFCompare` files contain functions to compare two sets of data directly.
They are not part of the standard workflow, but are useful for quick comparisons.

### ConcatNDiff
This function is a very quick way to compare mp4 files. 

It  gets the absolute value pixel to pixel difference of each frame, and concatenates it to the two original videos side by side.

## ConcatNxM
This function simply stitches videos on a grid with ***N*** rows and ***M*** columns.

### WRFSmoothDiff
This is a slightly more advanced way of comparing two sets of data.

It gets the difference directly from the wrfout files, and then animates the result using a divergent colourscale.
If the flag ***smooth*** is set to 1, it smooths the data before making the diff, so that slight positional changes are not as strongly reflected in the output.


## Run

This is now deprecated, and should not be used... everything is done through the csf script.
<details><summary>The old readme is kept here for reference.</summary>
This is hopefully the only script you will have to tweak to obtain the animations you are looking for.

It consist on a simple call to **Animate**, with all the sensible variables for which diagnostics are required.

These should simply be put in ***wvarlist***, and the directory path to your wrfout files should be set in ***dir_path***.
</details>


# Testing new code

In case there is no access to the csf, but you do have access to some `wrfout` files, you can run the code directly skipping the submition script.

The script `csf.py` is programmed to accept arguments, so you can call it with
```
python csf.py --task=diagnostic --var=SeaLevelPressure --dir_path=/my/wrfout/files/dir --outdir=Test_Control/
```

Alternatively, you can tweak and use the `tests/test.py` script.
The script has the advantage of being able to call `csf.py` with many arguments.
It assumes you have wrfout files in `tests/wrfdata/`, and places the results in `tests/results/`.

Modify the inputs for your test in the `all_args` list, and run with
```
python tests/test.py
```


# Conda environment

Make sure you have the conda environment set up and active before you call `csf.py` or `test.py`.

If you do not have the environment, make sure you have anaconda/miniconda/micromamba installed.
This will install it with defaults:
```
echo | "${SHELL}" <(curl -L micro.mamba.pm/install.sh)
source ~/.bashrc
```
Then you can create and activate the environment with
```
micromamba env create --name wrf-py-env --file environment.yml
micromamba activate wrf-py-env
```
You are now set up to use the code.
