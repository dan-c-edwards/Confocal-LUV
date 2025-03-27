"""
@author: Dan Edwards, Univeristy of Edinburgh, dan.edwards@ed.ac.uk
"""
# Input the correctly formatted csv/xlsx and a plot is exported with a Hill line fit.
# The purpose of this code is to plot the processed data from the confocal measurements formatted in three columns.
# The csv or xlsx file should be formatted with columns X-axis, Y-axis, SD.
# Check if the x-axis is required to be on a logarithmic scale (line 92).
# To adjust the Hill line fit the Vmax, Kd, and n values can be adjuste (line 50).
# The plot with the Hill line fit is exported as an SVG file.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Set all fonts to Arial, including for LaTeX
plt.rcParams['font.family'] = 'Arial'  # Set all fonts to Arial
plt.rcParams['mathtext.fontset'] = 'custom'  # Use custom math font settings
plt.rcParams['mathtext.rm'] = 'Arial'  # Regular (rm) font to Arial
plt.rcParams['mathtext.it'] = 'Arial:italic'  # Italic font to Arial (if needed)
plt.rcParams['mathtext.bf'] = 'Arial:bold'  # Bold font to Arial

# Step 1: Read the Excel file
df = pd.read_excel(r"FILEDIRECTORY\FILENAME.xlsx")

# Step 2: Extract the relevant columns (ensure your Excel file has these columns)
x = df['Conc']  # corresponding csv column title for x-axis
y = df['Mean']  # corresponding csv column title for y-axis
y_sd = df['SD']  # Standard deviation (SD) for error bars

# Debugging: Check x values before filtering
print(f"Original x values: {x}")

# Ensure x contains only positive values and filter y and y_sd accordingly
valid_indices = x > 0
x = x[valid_indices]
y = y[valid_indices]
y_sd = y_sd[valid_indices]

# Debugging: Check filtered data
print(f"Filtered x values: {x}")
print(f"Filtered y values: {y}")
print(f"Filtered y_sd values: {y_sd}")
print(f"Min x: {min(x)}, Max x: {max(x)}")

# Define the Hill equation
def hill_equation(x, Vmax, Kd, n):
    return (Vmax * x**n) / (Kd**n + x**n)

# Manually input the Hill equation parameters
Vmax = 0.90052  # Example maximum response
Kd = 0.0101    # Example dissociation constant
n = 1.67481     # Example Hill coefficient (slope)

# Generate smooth x values for the fitted curve
x_smooth = np.logspace(np.log10(min(x)), np.log10(max(x)), 500)
y_fitted = hill_equation(x_smooth, Vmax, Kd, n)

# Debugging: Check ranges of x_smooth and y_fitted
print(f"Smooth x range: {min(x_smooth)} to {max(x_smooth)}")
print(f"Hill curve y_fitted range: {min(y_fitted)} to {max(y_fitted)}")

# Step 4: Plot the scatter plot with error bars
plt.figure(figsize=(14, 12))

# Error bars with custom thickness and color
plt.errorbar(x, y, yerr=y_sd, fmt='o', capsize=5, ecolor='black', elinewidth=2)

# Make dots larger and black
plt.scatter(x, y, s=150, c='black', zorder=5)  # s=100 makes dots larger, c='black' makes them black

# Plot the fitted Hill curve
plt.plot(x_smooth, y_fitted, color='red', linewidth=2)

# Step 5: Customize tick marks (thickness of 2 and length of 10 for both major and minor ticks)
plt.tick_params(axis='x', width=2, length=10, labelsize=30, which='both')  # X-axis ticks (major + minor)
plt.tick_params(axis='y', width=2, length=10, labelsize=30, which='both')  # Y-axis ticks (major + minor)

# Step 6: Customize the plot border (box around the plot)
plt.gca().spines['top'].set_linewidth(2)    # Top border thickness
plt.gca().spines['right'].set_linewidth(2)  # Right border thickness
plt.gca().spines['bottom'].set_linewidth(2) # Bottom border thickness
plt.gca().spines['left'].set_linewidth(2)   # Left border thickness

# Step 7: Set axis labels and title
plt.xlabel('Concentration of Ionomycin / % to lipid', fontsize=40)  # Appropriate axis label
plt.ylabel(r'$f_{\mathrm{normalised}}$', fontsize=55)  # Subscript "normalised"
plt.xticks(fontsize=40)  # Increase font size for x-axis ticks
plt.yticks(fontsize=40)  # Increase font size for y-axis ticks

# Step 8: Set the x-axis to logarithmic scale
plt.xscale('log')

# Optional: Add grid, title, and legend
plt.grid(False)  # Turn off the grid
plt.legend(fontsize=40)  # Add a legend

# Step 9: Export the plot as SVG without cutting off any of the plot
plt.tight_layout()  # Ensures the plot is fully contained within the figure
plt.savefig(r"FILEDIRECTORY/SAVENAME.svg", format='svg')

# Show the plot
plt.show()
