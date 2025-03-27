"""
@author: Dan Edwards, Univeristy of Edinburgh, dan.edwards@ed.ac.uk
"""

# The purpose of this code is to process and plot the raw data exported from the confocal measurements.
# Each run is composed of 10 data files but the number of files plotted can be selected using number_of_files.
# The x-axis is plotted as time and hence is dependent on the acquisition rate.
# In this case the data was acquired at 10,000 Hz hence the x values should by divded by 10,000. See time_values line 55.
# The plot is exported as an SVG file.

import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import matplotlib.ticker as ticker  # Import the ticker module

# Set all fonts to Arial, including for LaTeX
plt.rcParams['font.family'] = 'Arial'  # Set all fonts to Arial
plt.rcParams['mathtext.fontset'] = 'custom'  # Use custom math font settings
plt.rcParams['mathtext.rm'] = 'Arial'  # Regular (rm) font to Arial
plt.rcParams['mathtext.it'] = 'Arial:italic'  # Italic font to Arial (if needed)
plt.rcParams['mathtext.bf'] = 'Arial:bold'  # Bold font to Arial

# Path and filenames
path_A = r"FILESTEMLOCATION"
file_stem_A = "FILENAME" # Filename before the underscore
number_of_files = 2  # Number of files in the folder

def load_files_A(number_of_files):
    channelA_A = []  # Where channel A data will be stored
    
    for i in range(number_of_files):
        if i == 0:
            filename = os.path.join(path_A, file_stem_A)
        else:
            filename = os.path.join(path_A, f"{file_stem_A}_{i + 1:02d}")
        
        a = 0  # Row counter
        with open(filename) as csvDataFile:  # Opens the file as a CSV
            csvReader = csv.reader(csvDataFile, delimiter='\t')  # Assigns the loaded CSV file to csvReader.
            for row in csvReader:
                channelA_A.append(float(row[0]))  # Convert to float for numerical operations
                a += 1
        
        print(f"Loaded {filename}, which contains {a} rows.")
    
    channelA_arr_A = np.asarray(channelA_A, dtype=np.float32)  # Converts to numpy arrays for vector calculations.
    return channelA_arr_A

# Load data for Channel A
channelA_arr_A = load_files_A(number_of_files)

# Generate time values for the x-axis (divide indices by 10,000)
time_values = np.arange(len(channelA_arr_A)) / 10000

# Manual Y-axis limits (set to None for automatic limits)
manual_y_limits = (0, 400)  # Set Y-axis range to 0-400

# Plotting Channel A data
plt.figure(figsize=(8, 4))  # Make the figure larger
plt.plot(time_values, channelA_arr_A, marker='none', linestyle='-', color='black', label='Channel A Data')  # Line plot with markers
plt.xlabel('Time / s', fontsize=40)  # Increased font size for x-axis label
plt.ylabel('Intensity / photons s$^{-1}$', fontsize=40)  # Increased font size for y-axis label
plt.xticks(fontsize=40)  # Increase font size for x-axis ticks
plt.yticks(fontsize=40)  # Increase font size for y-axis ticks

# Set major ticks every 100 seconds (change from 15 to 100)
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(100))  # Major ticks at every 100 seconds

# Customize major tick appearance
plt.tick_params(axis='x', which='major', length=10, width=2)  # Major ticks with custom length and width
plt.tick_params(axis='y', which='major', length=10, width=2)  # Major ticks for y-axis

# Add gridlines if needed
plt.grid(False)  # Remove grid lines

# Apply manual Y-axis limits if specified, else keep automatic limits
if manual_y_limits is not None:
    plt.ylim(manual_y_limits)  # Set Y-axis limits manually

# Add a box around the plot with thickness 2
ax = plt.gca()  # Get current axes
for spine in ax.spines.values():
    spine.set_edgecolor('black')  # Set the color of the box (black)
    spine.set_linewidth(2)  # Set the thickness of the box

# Save the plot as an SVG file with versioning based on file_stem_A
def get_next_filename(base_filename):
    version = 1
    while os.path.exists(f"{base_filename}_v{version}.svg"):
        version += 1
    return f"{base_filename}_v{version}.svg"

# Define the base filename using the file_stem_A and get the next available filename
base_filename = os.path.join(path_A, file_stem_A)
filename = get_next_filename(base_filename)

# Save the plot as SVG with the versioned filename
plt.savefig(f"{filename}.svg", format="svg", bbox_inches='tight')

# Show the plot
plt.show()
