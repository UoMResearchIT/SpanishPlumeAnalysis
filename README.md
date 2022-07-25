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


### WRF Variables for diagnostics

- 4D -> T -> Temperature °C -- Supposed to be K, but value range [-20,60] doesn't add up...
- 4D -> P -> Pressure Pa
- 4D -> U -> X wind component
- 4D -> V -> Y wind component
- Dewpoint?