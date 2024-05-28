# TidalPhaseFinder
TideFinder is a Python script designed to determine the tidal phase and amplitude of a specific timestamp using tide data. The script reads a CSV file containing tide information and calculates the current tide phase (ebbing or flooding), sub-tides (High tide, 3 stages of Ebb tide, 3 stages pf Flood tide), and tide amplitudes.

###################################################################
Features

    - Load tide data from a CSV file.
    - Determine the closest high and low tides around a specified time.
    - Calculate the tide type (Ebbing or Flooding).
    - Classify tides into Neap, Middle, or Spring tides based on amplitude (to be updated!).
    - Divide tide wave into sub-tides (Low tide, F1, F2 F3, High tide, E1, E2, E3).
    - Identify the specific sub-tide at a given timestamp. 
    
###################################################################
Usage

Ensure your CSV file has the following columns:

    -Date (in dd/mm/yyyy format)
    -Time (in HH:MM:SS format)
    -Height (Tide height in meters)
    -Tide (High-tide or Low-tide)

Example of CSV file with tidal information: 

 Date,	Time,	Height,	Tide
 01/01/2016,	01:11:00,	1.54,	Low-tide
 01/01/2016,	07:41:00,	3.36,	High-tide
 01/01/2016,	13:50:00,	1.51,	Low-tide
 01/01/2016,	20:16:00,	3.15,	High-tide

Example

from tide_finder import TideFinder

time_to_find = '2024-02-08 12:00:00'
tide_filepath = 'path_to_your_tides_csv_file.csv'

tide_finder = TideFinder(time_to_find, tide_filepath)
print(f"Tide type: {tide_finder.tide_type}")
print(f"Subtide name: {tide_finder.tide.subtide_name}")
print(f"Amplitude between peaks: {tide_finder.amplitude_between}")
print(f"Super tide: {tide_finder.super_tide}")

