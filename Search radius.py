#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from scipy.stats import norm, kurtosis
from scipy.stats import gaussian_kde
import arcpy
from arcpy.sa import KernelDensity

# Prompt the user to input data source and filename
data_source = input("Enter the data source: ")
filename = input("Enter the filename: ")

# Load data from CSV
data = pd.read_csv(data_source + '\\' + filename + '.csv')

# Convert the event_date column to datetime
data['event_date'] = pd.to_datetime(data['event_date'])

# Prompt the user to input the start and end dates for the period of interest
start_date = pd.to_datetime(input("Enter the start date (YYYY-MM-DD): "))
end_date = pd.to_datetime(input("Enter the end date (YYYY-MM-DD): "))

# Prompt the user to input the sub-event type
sub_event_type = input("Enter the sub-event type (violence, non-violence, or both): ")

# Filter the data within the specified period and sub_event_type
if sub_event_type.lower() == "violence":
    filtered_data = data[
        (data['event_date'] >= start_date) &
        (data['event_date'] <= end_date) &
        (~data['sub_event_type'].str.contains('peaceful protest', case=False, na=False)) &
        (~data['sub_event_type'].str.contains('protest with intervention', case=False, na=False))
    ]
elif sub_event_type.lower() == "non-violence":
    filtered_data = data[
        (data['event_date'] >= start_date) &
        (data['event_date'] <= end_date) &
        (data['sub_event_type'].str.contains('peaceful protest', case=False, na=False))
    ]
else:  # sub_event_type is "both"
    filtered_data = data[
        (data['event_date'] >= start_date) &
        (data['event_date'] <= end_date)
    ]

# Determine distribution type based on mean, median, skewness, and kurtosis
latitude = filtered_data['latitude']
longitude = filtered_data['longitude']

# Distribution determination
mean = np.mean([*latitude, *longitude])
median = np.median([*latitude, *longitude])
skewness = np.abs(norm.fit([*latitude, *longitude])[0])
kurtosis_val = kurtosis([*latitude, *longitude], fisher=False)

mean_threshold = 5
skewness_range = 0.5
kurtosis_range = 0.5

if abs(mean - median) <= (mean_threshold * mean / 100) and -skewness_range <= skewness <= skewness_range and (3 - kurtosis_range) <= kurtosis_val <= (3 + kurtosis_range):
    print("Data follows a normal distribution")
    is_normal_distribution = True
else:
    print("Data does not follow a normal distribution")
    is_normal_distribution = False

# Bandwidth estimation
if is_normal_distribution:
    # Bandwidth estimation using Silverman's rule of thumb for normal distribution
    bandwidth_silverman = 0.9 * min(np.std(latitude), np.std(longitude)) * len(latitude) ** (-0.2)
    bandwidth_non_normal_sj = np.inf  # Set Sheather and Jones' bandwidth to infinity for comparison
    bandwidth_non_normal_bowman = np.inf  # Set Bowman and Azzalini's bandwidth to infinity for comparison
else:
    # Bandwidth estimation using Sheather and Jones' method for non-normal distribution
    bandwidth_sj = np.power(1.06 * np.std([*latitude, *longitude]) * len(latitude) ** (-0.2), 0.5)

    # Bandwidth estimation using Bowman and Azzalini's rule for non-normal distribution
    IQR = np.percentile([*latitude, *longitude], 75) - np.percentile([*latitude, *longitude], 25)
    std_dev = np.std([*latitude, *longitude])
    n = len([*latitude, *longitude])
    bandwidth_bowman = min(IQR / 1.34, std_dev) * (n ** (-1/5))

    bandwidth_silverman = np.inf  # Set Silverman's bandwidth to infinity for comparison

# Determine the bandwidth based on distribution type
if is_normal_distribution:
    bandwidth_non_normal = bandwidth_sj
    print("Bandwidth (Sheather and Jones):", bandwidth_sj)
    print("Bandwidth (Bowman and Azzalini):", bandwidth_bowman)
else:
    bandwidth_non_normal = bandwidth_bowman
    print("Bandwidth (Bowman and Azzalini):", bandwidth_bowman)
    print("Bandwidth (Sheather and Jones):", bandwidth_sj)
    
print("Bandwidth (Silverman's rule of thumb):", bandwidth_silverman)

# Choose the bandwidth with the minimal value
bandwidth = min(bandwidth_silverman, bandwidth_non_normal)

print("Selected Bandwidth:", bandwidth)

# Prompt the user to input the output path and output name
output_path = input("Enter the output path: ")
output_name = input("Enter the output name: ")

# Save filtered data as a new feature class
output_fc = output_path + '\\' + output_name + '.shp'
arcpy.management.CreateFeatureclass(
    arcpy.os.path.dirname(output_fc),
    arcpy.os.path.basename(output_fc),
    "POINT",
    spatial_reference=arcpy.SpatialReference(4326)
)

# Open an insert cursor
with arcpy.da.InsertCursor(output_fc, ['SHAPE@XY']) as cursor:
    # Iterate over filtered data and insert points
    for _, row in filtered_data.iterrows():
        point = arcpy.Point(row['longitude'], row['latitude'])
        cursor.insertRow([(point.X, point.Y)])

# Perform Kernel Density
output_raster = output_path + '\\' + "kernel_density.tif"
kernel_density = KernelDensity(output_fc, 'NONE', bandwidth)
kernel_density.save(output_raster)

# Check if the operation was successful
if arcpy.Exists(output_raster):
    print("Kernel Density calculation completed successfully.")
else:
    print("Kernel Density calculation failed.")

