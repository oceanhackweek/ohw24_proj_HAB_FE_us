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
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap

st.title('OceanHackWeek: Bloom and Gloom Dashboard')
st.subheader('Application to showcase Algal Bloom and Harmful Algal Bloom Data!')
st.write('---')

with st.sidebar:
    st.header('Project Overview')

    st.subheader('Project Goal')
    st.write("Use PACE data to create user-interactive visuals")
    st.subheader('Source Data')
    st.write('PACE OCI Level-3 Global Mapped Remote-Sensing Reflectance (RRS) - NRT Data, version 2.0, NASA Earthdata')
    st.write('---')

    ### TODO - finish this

    selected_dates = st.date_input(
        'Select a Date Range',
        value = (datetime.date(2024, 7, 1), datetime.date(2024, 7, 2)),
        min_value = datetime.date(2024, 7, 1),
        max_value = datetime.date(2024, 8, 25),
        format = "YYYY-MM-DD",
        label_visibility = "visible"
        )

# check dates
if len(selected_dates) == 1:
    raise ValueError("Please select two different dates")
elif abs((selected_dates[1] - selected_dates[0]).days) > 5:
    raise ValueError("Please select a date range of 5 days or less")

# dask setup
# run the following in terminal before spinning up the app
# coiled login --token 48c0361f39984d7b8bab62f3252a5d7e-e6c38c5e8b15f967b104cf58ee289f4066ccd330

# the following code was created by the respective data team with a few updates
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

# Create y-coordinates for each dataset
y_indices = np.arange(rrs_values.shape[0])  # Create an array of dataset indices

def plot_3d_graph(wavelengths, y_indices, rrs_values):
    # Create a new figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot in 3D space using a single color (e.g., slategray)
    for dataset_index in range(rrs_values.shape[0]):
        ax.plot(wavelengths, np.full_like(wavelengths, y_indices[dataset_index]), rrs_values[dataset_index], color='slategray')

    # Set axis labels
    ax.set_xlabel('Wavelength')
    ax.set_ylabel('Days since 2024-07-01')
    ax.set_zlabel('Rrs')

    # Rotate the plot 45 degrees along the Y-axis
    ax.view_init(elev=35, azim=-60)

    # Return the figure object to use in Streamlit
    return fig

# Plot the 3D graph
fig = plot_3d_graph(wavelengths, y_indices, rrs_values)
# Show the plot in Streamlit
st.pyplot(fig)

col1a, col2b = st.columns([15, 15])
with col1a:
    # Make Chlorophyll map
    results_chl = earthaccess.search_data(
        short_name="PACE_OCI_L3M_CHL_NRT",
        granule_name="PACE_OCI.20240808.L3m.DAY.CHL.V2_0.chlor_a.4km.NRT.nc",
    )

    def process_and_viz_chl(granule_chl):
        # Use dask for lazy loading
        file = earthaccess.open(granule_chl)
        ds = xr.open_dataset(file[0], engine='h5netcdf')

        # Subset the dataset within the specified region
        subset = ds.sel(lon=slice(-159.5, -157.5), lat=slice(27.5, 26))
        chla = subset["chlor_a"]

        # Define the colors: dodgerblue to white to forest green
        colors = ['#0A548E', 'white', 'forestgreen']

        # Create the custom colormap
        custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', colors)

        # Set the figure size to [12, 20]
        fig1 = plt.figure(figsize=(12, 20))

        # Plot the chlorophyll-a concentration using the custom colormap, but without a colorbar
        artist = chla.plot(cmap=custom_cmap, vmax=0.3, add_colorbar=False)

        # Set the aspect ratio to be equal
        plt.gca().set_aspect("equal")

        # Add a custom, smaller colorbar
        cbar = plt.colorbar(artist, ax=plt.gca(), aspect=10, pad=0.02)
        cbar.ax.tick_params(labelsize=8)  # Optional: adjust tick label size
        cbar.ax.set_ylabel('Chlorophyll concentration\n OCI Algorithm (mg/m^3)', fontsize=12)
        return fig1

    fig1 = process_and_viz_chl(results_chl)

    st.pyplot(fig1)