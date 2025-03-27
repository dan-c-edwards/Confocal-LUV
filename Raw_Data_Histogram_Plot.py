"""
@author: Dan Edwards, Univeristy of Edinburgh, dan.edwards@ed.ac.uk
"""
# The purpose of this code is to plot the raw data from the confocal measurements as a distribution histogram.
# The data is processed by counting the number of events at each acquisition point and plotting a disbution histogram.
# The histogram is shortened by adding a manual threshold which only plots counts with the number of events above the threshold.
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
path_A = r"FILELOCATION"
file_stem_A = "FILENAME"  # Filename before the underscore
number_of_files = 10  # Number of files in the folder

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

def plot_histogram(data, bins=50, xlim=None, ylim=None, xlabel="Channel A Value", ylabel="Frequency", title=None, 
                   xtick_distance=None, bin_color='blue', bottom_threshold=None, top_threshold=None, box_thickness=2):
    """
    Plot a histogram with customizable bins, axis limits, x-tick spacing, and threshold filter.

    Parameters:
    - data: Data to plot
    - bins: Number of bins or bin edges (can be an integer or a list/array of edges)
    - xlim: Tuple (xmin, xmax) for x-axis limit
    - ylim: Tuple (ymin, ymax) for y-axis limit
    - xlabel: Label for the x-axis
    - ylabel: Label for the y-axis
    - title: Title of the histogram (default is None)
    - xtick_distance: Distance between x-tick marks (if None, automatically determined)
    - bin_color: Single color for all bins (e.g., 'blue') or list of colors for each bin
    - bottom_threshold: Minimum value of data to be included (if None, no filtering is applied)
    - top_threshold: Maximum value of data to be included (if None, no filtering is applied)
    - box_thickness: Thickness of the box (spines) around the plot
    """
    # Apply the bottom and top threshold filters (if provided)
    if bottom_threshold is not None:
        data = data[data >= bottom_threshold]
    if top_threshold is not None:
        data = data[data <= top_threshold]

    # Adjust bins based on xlim if it's provided
    if xlim:
        xmin, xmax = xlim
        # Ensure bins stay within the xlim range
        bins = np.linspace(xmin, xmax, bins)

    # Plot histogram
    plt.figure(figsize=(8, 8))  # Changed plot size to (8, 8)
    
    # If a single color is provided for all bins, use that color
    if isinstance(bin_color, str):
        n, bins_edges, patches = plt.hist(data, bins=bins, edgecolor='black', alpha=0.7, color=bin_color)
    # If bin_color is a list of colors (same length as number of bins), use them
    elif isinstance(bin_color, list) and len(bin_color) == len(bins):
        n, bins_edges, patches = plt.hist(data, bins=bins, edgecolor='black', alpha=0.7, color=bin_color)
    else:
        # If bin_color is not valid, default to blue
        n, bins_edges, patches = plt.hist(data, bins=bins, edgecolor='black', alpha=0.7, color='blue')

    # Customization for the x and y limits
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    
    # Set labels with larger font sizes
    plt.xlabel('Intensity / photons s$^{-1}$', fontsize=40)
    plt.ylabel('Count', fontsize=40)  # Custom y-axis label
    if title:
        plt.title(title, fontsize=40)
    else:
        plt.title('')  # Explicitly hide the title if None
    
    # Set tick label sizes
    plt.xticks(fontsize=40)
    plt.yticks(fontsize=40)

    plt.tick_params(axis='x', which='major', length=10, width=2)  # Major ticks with custom length and width
    plt.tick_params(axis='y', which='major', length=10, width=2)  # Major ticks for y-axis

    # Remove gridlines
    plt.grid(False)

    # Optionally format the tickers (if desired)
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x)}'))  # Format X axis as integers
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x)}'))  # Format Y axis to integers

    # Customize x-ticks if xtick_distance is provided
    if xtick_distance is not None:
        xticks = np.arange(np.min(data), np.max(data), xtick_distance)
        plt.xticks(xticks)

    # Add a box around the plot with thickness of 2
    for spine in plt.gca().spines.values():
        spine.set_linewidth(box_thickness)  # Set box thickness to 2

    # Adjust the layout to ensure nothing is cut off
    plt.tight_layout()

    # Save the plot to an SVG file using file_stem_A
    output_file = f"{file_stem_A}_histogram2.svg"
    plt.savefig(output_file, format='svg')  # Save as SVG
    
    # Show the plot
    plt.show()

# Example of plotting the histogram with custom parameters
# Setting a bottom threshold value to filter out data below it (e.g., bottom_threshold = 30) 
# and a top threshold to filter out values above a certain threshold (e.g., top_threshold = 200)
plot_histogram(channelA_arr_A, bins=50, xlim=(50, 250), ylim=(0, 750), 
               xtick_distance=50, bin_color='grey', bottom_threshold=50, top_threshold=200, 
               box_thickness=2)
