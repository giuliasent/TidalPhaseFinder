# TidalPhaseFinder
 Define the tidal condition of a given timestamp

 The code is firstly tested on a jupiter noteboook and, once it works, it is saved in a python script. The jupiter noteboooks are generally the most updated versions because I often forget to update the corresponding .py files. 

The "TidalPhaseFinder_v1.py" correctly associate the tidal condition of a given timestamp or list of timestamps.
This first version do not account for Slack water. It justt find the peaks (before and after) and divide the duration in 3 equal time windows. It discriminate if the water is Flodding (F) or Ebbing (E)

TidalPhaseFinder_v3 includes classification of Sping, Neap and  Middle  tides, discriminated by amplitude. 
Neap tides = amplitude <1.2m
Middle tides 1.2m < amplitude < 2m
Spring tides = amplitude > 2m 