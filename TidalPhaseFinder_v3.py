"""
Updated: 2024-02-08 
3 hours of slack water
"""

import pandas as pd
import datetime as dt
from datetime import datetime


class Tide:
    def __init__(self, begin, end, type, begin_type, end_type, time_slack = dt.timedelta(minutes=60)):
        "slack water: 2 hours around the peak"
        self.begin_time = begin + time_slack
        self.end_time = end - time_slack
        self.duration = self.end_time - self.begin_time
        self.type = type
        self.tide_before = begin_type
        self.tide_after = end_type

    def define_subtides(self, N_subtides=3):
        # add slack water, both high and low
        try:
            if self.type == "Ebbing":
                self.subtides_names = ["E1", "E2", "E3"]
            elif self.type == "Flooding":
                self.subtides_names = ["F1", "F2", "F3"]

            else:
                raise ValueError("Tide type must be either Ebbing, Flooding")
            self.subtides = {}
        

            for i in range(N_subtides):
                self.subtides[self.subtides_names[i]] = SubTide(self.begin_time + i * self.duration / N_subtides,
                                                            self.begin_time + (i + 1) * self.duration / N_subtides,
                                                            self.type)
        except:
            print("Timestamp falls inbetween two subtides")

class SubTide:
    def __init__(self, begin, end, type):
         self.begin = begin
         self.end = end
         self.duration = end - begin
         self.type = type


class TideFinder:
    def __init__(self, time_to_find, filepath):
        self.tide = None
        self.subtide_name = None
        self.time_to_find = pd.to_datetime(time_to_find)
        self.filepath = filepath
        self.load_tide_table()
        self.find_peaks_type_amplitudes()
        self.time_from_last_low_peak()
        self.find_tide_type()
        self.amplitude_between_peaks()
        self.initialize_tide_and_subtides()
        self.find_final_subtide()

    def load_tide_table(self):
        self.tide_table = pd.read_csv(self.filepath, parse_dates=[['Date', 'Time']], dayfirst=True)
        #convert to datetime
        self.tide_table['Date_Time'] = pd.to_datetime(self.tide_table['Date_Time'], format='%d/%m/%Y %H:%M:%S')
    
        
    def find_peaks_type_amplitudes(self):
        "Find the closest time before and after the time to find"
        self.time_nearest_before = min(self.tide_table.Date_Time, key=lambda x: (x>self.time_to_find, abs(x-self.time_to_find)))
        self.time_nearest_after = min(self.tide_table.Date_Time, key=lambda x: (x<self.time_to_find, abs(x-self.time_to_find)))
        self.tide_before = self.tide_table.loc[(self.tide_table["Date_Time"]==str(self.time_nearest_before))]["Tide"].values
        self.tide_after = self.tide_table.loc[(self.tide_table["Date_Time"]==str(self.time_nearest_after))]["Tide"].values
        self.amplitude_before = self.tide_table.loc[(self.tide_table["Date_Time"]==str(self.time_nearest_before))]["Height"].values
        self.amplitude_after = self.tide_table.loc[(self.tide_table["Date_Time"]==str(self.time_nearest_after))]["Height"].values

    def find_tide_type(self):
        if self.tide_before == "High-tide":
            self.tide_type = 'Ebbing'
        elif self.tide_before == "Low-tide":
            self.tide_type = 'Flooding'
    
    def time_from_last_low_peak(self):
        "find the time from the last low peak"
        self.low_peaks = self.tide_table[self.tide_table.Tide=='Low-tide']
        self.low_peak_before = min(self.low_peaks.Date_Time, key=lambda x: (x>self.time_to_find, abs(x-self.time_to_find)))
        self.time_from_low_peak = self.time_to_find - self.low_peak_before

    def amplitude_between_peaks(self):
        self.amplitude_between = abs(self.amplitude_after - self.amplitude_before)
        if self.amplitude_between <= 1.5:
            self.super_tide = "Neap tide"
        elif 1.5<self.amplitude_between <= 3:
            self.super_tide = "Middle tide"
        elif self.amplitude_between > 3:
            self.super_tide = "Spring tide"

    def initialize_tide_and_subtides(self):
        self.tide = Tide(self.time_nearest_before, self.time_nearest_after, self.tide_type, self.tide_before, self.tide_after)
        self.tide.define_subtides()

    def find_final_subtide(self, slack_time=dt.timedelta(minutes=60)):
        for subtide_name in self.tide.subtides_names:

            if (self.tide.subtides[subtide_name].begin <= self.time_to_find <= self.tide.subtides[subtide_name].end) == True:
                self.tide.subtide_name = subtide_name

            elif (self.tide.end_time < self.time_to_find < self.tide.end_time + slack_time) & (self.tide.tide_after == "High-tide") == True:
                self.tide.subtide_name = "High tide"
            elif(self.tide.begin_time - slack_time < self.time_to_find < self.tide.begin_time) & (self.tide.tide_before == "High-tide") == True:
                self.tide.subtide_name = "High tide"

            elif(self.tide.end_time < self.time_to_find < self.tide.end_time + slack_time) & (self.tide.tide_after == "Low-tide") == True:
                self.tide.subtide_name = "Low tide"
            elif(self.tide.begin_time - slack_time < self.time_to_find < self.tide.begin_time) & (self.tide.tide_before == "Low-tide") == True:
                self.tide.subtide_name = "Low tide"