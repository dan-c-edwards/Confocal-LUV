"""
@author: Dan Edwards, Univeristy of Edinburgh, dan.edwards@ed.ac.uk
"""

# The purpose of this code is to process and export the raw data exported from the confocal measurements.
# Each experiment is composed of a number of run "expnum" and each run is composed of 10 files "number_of_files".
# The data is processed by counting the number of events which have a magnitude higher than a threshold.
# The range of thresholds are defined here between 20 and 50 "thresholds".
# These values are then exported into an xlsx file with additional columns to add specific conditions.

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

plt.rcParams['font.family'] = 'Arial'  # set all fonts to Arial

# Constants
exptitle = "769_"  # experiment title preceding numerical value
exptdate = "20250226"  # date used for data storage
expnum = 11 # number of experiments to be analysed
thresholds = [20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 160, 170, 180, 190, 200]  # List of thresholds to check
path_A = rf"U:\SCE\CHEM\Research Groups\Cockroft\Dan\_PDRA\01_Data\_Confocal\{exptdate}"
number_of_files = 10

# Base save file name in the format "exptdate - exptitle"
base_filename = f"{exptdate} - {exptitle}"

# Define function to create unique filenames (avoid overwriting existing files)
def get_unique_filename(path, base_filename, extension="xlsx"):
    """
    Check if a file exists and append a version number to avoid overwriting.
    """
    version = 1
    filename = f"{base_filename}.{extension}"
    file_path = os.path.join(path, filename)
    
    # Increment version number until a unique filename is found
    while os.path.exists(file_path):
        version += 1
        filename = f"{base_filename}_v{version}.{extension}"
        file_path = os.path.join(path, filename)
    
    return file_path

# Get the full file path with the unique name
excel_output_path = get_unique_filename(path_A, base_filename, extension="xlsx")

def load_files(file_stem):
    """
    Load data from files with a specific stem and return numpy arrays.
    """
    channelA_data = []
    channelB_data = []
    
    for i in range(number_of_files):
        filename = os.path.join(path_A, f"{file_stem}_{i+1:02d}" if i > 0 else file_stem)
        
        if not os.path.isfile(filename):
            print(f"File does not exist: {filename}")
            continue
        
        with open(filename) as csvDataFile:
            csvReader = csv.reader(csvDataFile, delimiter='\t')
            for row in csvReader:
                channelA_data.append(float(row[0]))  # Convert to float for numerical operations
                channelB_data.append(float(row[1]))
    
    channelA_arr = np.asarray(channelA_data, dtype=np.float32)
    channelB_arr = np.asarray(channelB_data, dtype=np.float32)
    return channelA_arr, channelB_arr

def count_events_above_threshold(channelA_arr, threshold):
    """
    Count the number of events above the threshold.
    """
    return np.sum(channelA_arr > threshold)

# File stems
file_stems = [f"{exptitle}{i:02d}" for i in range(1, expnum + 1)]

# Dictionary to store events for each threshold
events_dict = {threshold: [] for threshold in thresholds}

for file_stem in file_stems:
    channelA_arr, _ = load_files(file_stem)
    for threshold in thresholds:
        events = count_events_above_threshold(channelA_arr, threshold)
        events_dict[threshold].append(events)
        print(f"{file_stem} - Number of events above {threshold}: {events}")

# Prepare the data for exporting
data = {
    'Datafile': [f'{i:02d}' for i in range(1, expnum + 1)],
    'Contents': [''] * expnum,  # Blank columns
    'Conc': [''] * expnum,      # Blank columns
    'Incub': [''] * expnum,     # Blank columns
    'Flow': [''] * expnum,      # Blank columns
}
for threshold in thresholds:
    data[f'Events above {threshold}'] = events_dict[threshold]

df = pd.DataFrame(data)

# Export to Excel (ensuring no overwrite)
df.to_excel(excel_output_path, index=False)

print(f"Data successfully exported to {excel_output_path}")
