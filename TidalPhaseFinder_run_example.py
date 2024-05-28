from TidalPhaseFinder_v3 import *
from datetime import datetime
import pandas as pd

path = "/home/giulia/Documents/PhD_Onedrive/"

filepath = path+"Data/TAGUS/ancillary/LisboaFCUL2016_2023.csv"
timestamps_file = pd.read_csv(path+"Data/TAGUS/In_situ/compiled_data/Tagus_all_data_compiled.csv", parse_dates=['start_timestamp_utc'], dayfirst=True)
df_in = pd.to_datetime(timestamps_file['start_timestamp_utc'], format="%d-%m-%Y %H:%M")
df_in = pd.to_datetime(df_in)

tide_condition = []
super_tide = []
amplitude = []
time_from_low_peak = []
for date in df_in:
    #if attribute error then it is because the time is not in the range of the tide table, skip it and append nan
    try:
        example = TideFinder(time_to_find=date, filepath=filepath)
        tide_condition.append(example.tide.subtide_name)
        #print(example.tide.subtide_name)
        super_tide.append(example.super_tide)
        amplitude.append(example.amplitude_between)
        time_from_low_peak.append(example.time_from_low_peak)
    except AttributeError:
        tide_condition.append("NaN")
        super_tide.append("NaN")
        amplitude.append("NaN")
        time_from_low_peak.append("NaN")
        continue

#merge lists into single dataframe using df_in as first columns
df_out = pd.DataFrame(list(zip(df_in, tide_condition, super_tide, amplitude, time_from_low_peak)), columns =['timestamp','tide_phase', 'tide_type', 'amplitude_between_peaks', 'time_from_low_peak'])
df_out.to_csv(path+"Data/TAGUS/In_situ/compiled_data/is_tidal_phases_all_2h.csv", index=False, header=True)
