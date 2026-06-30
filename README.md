# WRF Analysis Toolkit

This repo contains a set of scripts to generate diagnostics from WRF outputs, and to compare them with other WRF outputs.

## Table of contents
- [WRF Analysis Toolkit](#wrf-analysis-toolkit)
  - [Table of contents](#table-of-contents)
  - [Setup](#setup)
  - [Generating diagnostics](#generating-diagnostics)
  - [About the source code](#about-the-source-code)
    - [Animate](#animate)
    - [Plot2DField](#plot2dfield)
    - [SensibleVariables](#sensiblevariables)
    - [GetSensVar](#getsensvar)
    - [Special diagnostics](#special-diagnostics)
      - [TerrainPlots](#terrainplots)
      - [Frontogenesis](#frontogenesis)
      - [SkewT](#skewt)
    - [Direct comparison of outputs](#direct-comparison-of-outputs)
      - [ConcatNDiff](#concatndiff)
      - [ConcatNxM](#concatnxm)
      - [WRFSmoothDiff](#wrfsmoothdiff)
  - [Tests](#tests)
  - [Conda environment](#conda-environment)

## Setup

<details>
<summary>Set up your conda environment to meet the requirements.</summary>

- See [conda environment](#conda-environment) for instructions on how to set up the conda environment.

</details>

## Generating diagnostics

The `wrf_analysis_toolkit_cli.py` file is designed to be called as a cli.
You *always* have to pass these arguments:
- **task**, which can be *diagnostic*, *wrfcompare*, *mp4diff* or *mp4stitch*.
- **var**, which can be any of the predefined **SensibleVariables**.
- **dir_path**, which is the directory of the source files.
- **outdir**, which is the directory where outputs will be saved.

In some cases, you will also need to pass:
- **dirs**, which is the list of directories, when being compared.
- **files**, which is the list of names of files, when being compared.
- **labels**, which is the list of labels added when files are being compared or stitched.

The following are sample calls for this function:

*python wrf_analysis_toolkit_cli.py --task=diagnostic --var=Rain --dir_path=./MyData/ --outdir=./*

*python wrf_analysis_toolkit_cli.py --task=wrfcompare --var=SeaLevelPressure --dirs="Data1,Data2" --outdir=./ --difflabel=Data2-Data1*

*python wrf_analysis_toolkit_cli.py --task=mp4diff --var=DewpointTemp850 --dirs="./MP4_1,./MP4_2/" --labels="MP4_1,MP4_2,MP4Diff"*
*python wrf_analysis_toolkit_cli.py --task=mp4stitch --dirs="MyVideos" --files="f1,f2,f3,f4" --N=2 --M=2*

## About the source code

### Animate
This is the core of the diagnostic generation.
In this function all your wrfout files are loaded, the variables are extracted using **GetSensVar**, plotted using **Plot2DField**, and combined into an mp4.

*All* the files in ***dir_path*** will be loaded and combined, so make sure you want that.

The information on the diagnostic being generated should be provided in an ***svariable*** object, as defined in **SensibleVariables**.

Should you wish to override the default windbarb overlapping defined for some **SensibleVariables**, the call to this function is the best place to do so.

By default, when the animation is processed and the mp4 is successfully generated all png files are deleted. This can be controled with the flag ***cleanpng***.

### Plot2DField
This function simply plots a given variable (***var***) with the metadata found in the ***svariable*** object.

A flag for ***windbarbs*** may be turned on, for which the wind components ***u*** and ***v*** must be given as inputs too.

### SensibleVariables
This defines a class for variables with more sensible names than the ones used in wrf, which makes it a bit more amicable.

The object is basically composed of metadata for the diagnostics that are of interest to this particular project, but the list can easily be expanded.

The information in each object is used as instructions in the extraction of the variable from netcdf files and during plotting.

Each of the variables has the attributes that describe the way the variable should be plotted, including the colour scale, units, title, range, type of plot, annotations (like wind-barbs or contour-lines), and potentially overlapping variables.

See the description of each predefined **svariable** inside the file.

### GetSensVar
This function is an adaptation of wrf-python's *getvar*, but makes it simpler to obtain the diagnostics of interest, and uses the information in **svariable** objects

It deals with all the tecnical details on how to load the variables from the netcdf file so that they can be passed to the **Plot2DField** function.
This includes loading the wind velocity components when ***windbarbs*** is set to 1.

During this process, it also takes care of some variable computation, which is not universally implemented in *getvar*.

The outputs are the processed variable ***var***, the wind velocity components ***u*** and ***v*** (if windbarbs=0 these will be None), and the raw variable values ***varv*** (for use in *isdif* **svariable** computation).


### Special diagnostics

The following diagnostics have special functions to deal with them, but the diagnostic generation is still done through the wrf_analysis_toolkit_cli.py script.

#### TerrainPlots
These do not require animation nor the whole of the wrfout files, so they have a special function to deal with them.
They use the same **Plot2DField** function, and add annotations to the plot.

#### Frontogenesis
This is a special diagnostic that requires a bit of extra computation. The function is called from within GetSensVar, and passed to Animate as the other diagnostics.

#### SkewT
SkewTs are a completely different plotting style, and so they have a special function to deal with them,
which uses the [metpy](https://unidata.github.io/MetPy/latest/api/index.html) library.
They also combine a lot of wrf variables, so they are not generated in the same way as the other diagnostics.
The function is called from Animate, as an alternative to the standard Plot2DField for other diagnostics.


### Direct comparison of outputs

The `MP4Compare` and `WRFCompare` files contain functions to compare two sets of data directly.
They are not part of the standard workflow, but are useful for quick comparisons.

#### ConcatNDiff
This function is a very quick way to compare mp4 files. 

It  gets the absolute value pixel to pixel difference of each frame, and concatenates it to the two original videos side by side.

#### ConcatNxM
This function simply stitches videos on a grid with ***N*** rows and ***M*** columns.

#### WRFSmoothDiff
This is a slightly more advanced way of comparing two sets of data.

It gets the difference directly from the wrfout files, and then animates the result using a divergent colourscale.
If the flag ***smooth*** is set to 1, it smooths the data before making the diff, so that slight positional changes are not as strongly reflected in the output.


## Tests
There are two ways in which the code can be currently tested, with slightly different objectives.

The tests inside the `tests/integration` folder are designed to run independently, and detect both coverage and code errors. They are run using pytest, and assert the existence of the output files, but do not check their content.

The tests inside the `tests/human_checks` folder are designed to produce outputs that can be visually checked by a human.

Both sets of tests are only integration tests, and do not check the individual functions. They are designed to be run inside a container, which is built using the Dockerfile in the root of this repo.
A compose file is provided for convenience, which will build the container and run the tests inside it.
You may run the tests by first mounting into the test directory (`cd tests/`) and then running:
```
docker compose up --build pytest-coverage
```
or
```
docker compose up --build human-checks
```

You'll find further information in the compose file.


## Conda environment

If you are using this code directly on your machine (as opposed to using the container described in [tests](#tests)), make sure you have the conda environment set up and active before you call `wrf_analysis_toolkit_cli.py` or `test.py`.

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
