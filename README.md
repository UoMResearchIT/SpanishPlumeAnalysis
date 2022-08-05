# About the scripts

## Run
This is hopefully the only script you will have to tweak to obtain the animations you are looking for.

It consist on a simple call to **Animate**, with all the sensible variables for which diagnostics are required.

These should simply be put in ***wvarlist***, and the directory path to your wrfout files should be set in ***dir_path***.

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

See the description of each predefined **svariable** inside the file.

## GetSensVar
This function is an adaptation of wrf-python's *getvar*, but makes it simpler to obtain the diagnostics of interest, and uses the information in **svariable** objects

It deals with all the tecnical details on how to load the variables from the netcdf file so that they can be passed to the **Plot2DField** function.
This includes loading the wind velocity components when ***windbarbs*** is set to 1.

During this process, it also takes care of some variable computation, which is not universally implemented in *getvar*.

The outputs are the processed variable ***var***, the wind velocity components ***u*** and ***v*** (if windbarbs=0 these will be None), and the raw variable values ***varv*** (for use in *isdif* **svariable** computation).

## ConcatNDiff
This function is a very quick way to compare mp4 files. 

If the flag ***diff*** is set to 0, it simply concatenates the two mp4 files side by side. 

If ***diff*** is set to 1, it also gets the absolute value pixel to pixel difference of each frame, and concatenates it too.





# SpanishPlumeAnalysis
Visualization and comparison of WRF data on the Spanish Plume, modifying the geographical terrain and or heat/moisture flux over the spanish peninsula.

## Discussion with Dave Shultz (2022-07-21)
Spanish Plume -- Weather patter usually favourable to light thunderstorm and heavy rains

Historically, Spain's high regions were thought to warm the air up, and add moisture

David: That doesnt seem to be true, It most likely originated in North Africa and was not affected as much over Spain.

Preliminar results show that it is related to the plateou, but because it descends (therefore increases P and T), not because it was warmed up over spain.

A way to proove it would be to check whether wiping out the spanish plateu would change anything.

- Get rid of heights.
- Get rid of the heat/moisture flux and check whether spain did add heat or not.


## Expected outcomes
Interest in how to display info to be able to diagnose.

### Diagnostics

- 1,2 -> Air temperature and dewpoint temperature at the surface and 850 hPa
- 3,4 -> Static stability (difference in air temperature) T(700 hPa) – T(500 hPa) and T(850 hPa) – T(700 hPa)
- 5 ->   Sea-level pressure and Precipitation at surface and wind barbs
- 5/6?   500-hPa geopotential height (wind barbs)
- 7 ->   CAPE (convective available potential energy), CIN (convective inhibition)


## Questions
Is static stability really just Temp1-Temp2? Implementations elsewhere suggest otherwise...
Rain was computed as the sum of RAINC and RAINNC.. is that correct? Fussy literature...