import streamlit as st
import dask
import earthaccess
import matplotlib.pyplot as plt
import tempfile
import os
import numpy as np
import xarray as xr
import pandas as pd
import cmocean
import coiled
import datetime

from matplotlib.colors import LinearSegmentedColormap


st.title('OceanHackWeek: Bloom and Gloom Dashboard')
st.subheader('Application to showcase Algal Bloom Hyperspectral Data!')
st.write('---')

with st.sidebar:
    st.header('Project Overview')
    st.subheader('Participants')
    st.write('Data Team: Ben, Farley, Phil')
    st.write('App Team: Adelle, Adam, Kasandra')
    st.subheader('Source Data')
    st.write('PACE OCI Level-3 Global Mapped Remote-Sensing Reflectance (RRS) - NRT Data, version 2.0, NASA Earthdata')
    st.write('---')

    ### TODO - finish this

    selected_dates = st.date_input(
        'Select a Date', 
        value = (datetime.date(2024, 7, 1), datetime.date(2024, 7, 2)), 
        min_value = datetime.date(2024, 7, 1), 
        max_value = datetime.date(2024, 8, 25), 
        format = "YYYY-MM-DD", 
        label_visibility = "visible"
        )
    
    add_selectbox = st.sidebar.selectbox(
        "Example Select Box",
        ("opt1", "opt2", "opt3")
    )

# check dates
if selected_dates[0] == selected_dates[1]:
    raise ValueError("Please select two different dates")
elif abs((selected_dates[1] - selected_dates[0]).days) > 5:
    raise ValueError("Please select a date range of 5 days or less")

# dask setup
# run the following in terminal before spinning up the app
# coiled login --token 48c0361f39984d7b8bab62f3252a5d7e-e6c38c5e8b15f967b104cf58ee289f4066ccd330

# the following code was created by the data team with a few updates 
# for interacability, all credit goes to them

# .netrc file is required for authentication (Please fill out with your earthdata login credentials)
auth = earthaccess.login()
# are we authenticated?
if auth.authenticated:
    st.write("Data Access Authenticated!")
if not auth.authenticated:
    # ask for credentials and persist them in a .netrc file
    raise ValueError("Authentication failed. Please check your .netrc file.")

tspan = (selected_dates[0].strftime("%Y-%m-%d"), selected_dates[1].strftime("%Y-%m-%d"))
# tspan = ("2024-07-01", "2024-08-25")
bbox = (-170, 23, -140, 33)
clouds = (0, 50)

# search for data
results = earthaccess.search_data(
    short_name="PACE_OCI_L3M_RRS_NRT",
    temporal=tspan,
    bounding_box=bbox,
    granule_name="PACE_OCI.*.L3m.DAY.RRS.V2_0.Rrs.0p1deg.NRT.nc",
)
# link where this code came from: https://docs.coiled.io/blog/processing-terabyte-scale-nasa-cloud-datasets-with-coiled.html#processing-on-the-cloud-with-coiled
@coiled.function(
    region="us-west-2",                  # Run in the same region as data
    environ=earthaccess.auth_environ(),  # Forward Earthdata auth to cloud VMs
    spot_policy="spot_with_fallback",    # Use spot instances when available
    arm=True,                            # Use ARM-based instances
    cpu=1,                               # Use Single-core instances
)
def process(granule):
    # Use dask for lazy loading
    combined_datasets = []
    with tempfile.TemporaryDirectory() as tmpdir:
        files = earthaccess.download(granule, tmpdir)
        # Iterate over all the datasets
        for file in files:
            # Open dataset
            ds = xr.open_dataset(file)
            # Rechunk the dataset after loading
            ds = ds.chunk({'lon': 'auto', 'lat': 'auto'})  # Use 'auto' or set specific sizes
            # Subset the dataset within the specified region and append to list
            subset = ds.sel(lon=slice(-159.5, -157.5), lat=slice(27.5, 26))
            combined_datasets.append(subset)

        # Concatenate all subsets along the 'dataset' dimension
        combined_dataset = xr.concat(combined_datasets, dim='dataset')

        # Calculate the mean Rrs value across lon and lat for each dataset
        average_per_dataset = combined_dataset.mean(dim=['lon', 'lat']) 

        # Extract wavelengths and Rrs values at once to avoid repeated computation
        wavelengths = average_per_dataset['wavelength'].values
        rrs_values = average_per_dataset['Rrs'].compute()  # Trigger computation for all datasets

    return wavelengths, rrs_values

wavelengths, rrs_values = process(results)

# Assuming average_per_dataset is already created using Dask
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create y-coordinates for each dataset
y_indices = np.arange(rrs_values.shape[0])  # Create an array of dataset indices

# Plot in 3D space using a single color (e.g., slategray)
for dataset_index in range(rrs_values.shape[0]):
    ax.plot(wavelengths, np.full_like(wavelengths, y_indices[dataset_index]), rrs_values[dataset_index], color='slategray')

# Set axis labels
ax.set_xlabel('Wavelength')
ax.set_ylabel('Days since 2024-07-01')
ax.set_zlabel('Rrs')

# Rotate the plot 45 degrees along the Y-axis
ax.view_init(elev=35, azim=-60)

# Show the plot
st.pyplot(fig)