import streamlit as st
import earthaccess
import matplotlib.pyplot as plt
import tempfile
from PIL import Image
import numpy as np
import xarray as xr
import pandas as pd
import coiled
import datetime
# from mpl_toolkits.mplot3d import Axes3D


# Set page title
st.markdown("<h1 style='text-align: center;'>OceanHackWeek: Bloom and Gloom Dashboard</h1>", unsafe_allow_html=True)
# st.title('OceanHackWeek: Bloom and Gloom Dashboard')
# Set page description
# st.subheader('Application to showcase Algal Bloom and Harmful Algal Bloom Data!')
st.markdown("<h3 style='text-align: center;'>Application to showcase Algal Bloom and Harmful Algal Bloom Data!</h3>", unsafe_allow_html=True)
st.write('---')

# Sidebar
with st.sidebar:
    # Set sidebar title
    st.header('Project Overview')
    st.image("https://pace.oceansciences.org/images/layout/pace_l2_banner_txt_small.png")
    # Set sidebar description
    st.subheader('Project Goal')
    st.write("Use PACE data to create user-interactive visuals")
    st.subheader('Source Data')
    st.write('PACE OCI Level-3 Global Mapped Remote-Sensing Reflectance (RRS) - NRT Data, version 2.0, NASA Earthdata')
    st.write('---')

    # create date range picker
    selected_dates = st.date_input(
        'Select a Date Range for Hyperspectral Data',
        value = (datetime.date(2024, 8, 4), datetime.date(2024, 8, 8)),
        min_value = datetime.date(2024, 8, 1),
        max_value = datetime.date(2024, 8, 31),
        format = "YYYY-MM-DD",
        label_visibility = "visible"
        )
    # create sample date picker for Bloom v. No Bloom
    comp_date_1 = st.date_input(
        'Date for Bloom',
        value = (datetime.date(2024, 8, 4)),
        format = "YYYY-MM-DD",
        label_visibility = "visible"
        )
    comp_date_2 = st.date_input(
        'Date for No Bloom',
        value = (datetime.date(2024, 7, 19)),
        format = "YYYY-MM-DD",
        label_visibility = "visible"
        )

# check dates to ensure they are different and within 5 days
# raise error if dates are the same
if len(selected_dates) == 1:
    raise ValueError("Please select two different dates")
# raise error if dates are more than 5 days apart
elif abs((selected_dates[1] - selected_dates[0]).days) > 5:
    raise ValueError("Please select a date range of 5 days or less")

st.markdown(
    """
    <style>
    .gradient-text {
        background: linear-gradient(to right, #ef5350, #f48fb1, #7e57c2, #2196f3, #26c6da, #43a047, #eeff41, #f9a825, #ff5722);
        -webkit-background-clip: text;
        color: transparent;
        text-align: center;
        font-size: 2em;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<h1 class="gradient-text">3D Hyperspectral Data</h1>', unsafe_allow_html=True)

# dask setup
# run the following in terminal before spinning up the app
# coiled login --token 48c0361f39984d7b8bab62f3252a5d7e-e6c38c5e8b15f967b104cf58ee289f4066ccd330

# the following code was created by the respective data team with a few updates
# for interacability, all credit goes to them

# .netrc file is required for authentication (Please fill out with your earthdata login credentials)
auth = earthaccess.login()
# are we authenticated?
# if auth.authenticated:
    # st.write("Data Access Authenticated!")
if not auth.authenticated:
    # ask for credentials and persist them in a .netrc file
    raise ValueError("Authentication failed. Please check your .netrc file.")

# Set the search parameters
tspan = (selected_dates[0].strftime("%Y-%m-%d"), selected_dates[1].strftime("%Y-%m-%d"))
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
# create a function to process the data
def process(granule):
    # Use dask for lazy loading
    combined_datasets = []
    # Use a temporary directory to store the downloaded files
    with tempfile.TemporaryDirectory() as tmpdir:
        # Download the granule files
        files = earthaccess.download(granule, tmpdir)
        # Iterate over all the datasets
        for file in files:
            # Open dataset
            ds = xr.open_dataset(file)
            # Rechunk the dataset after loading
            ds = ds.chunk({'lon': 'auto', 'lat': 'auto'})  # Use 'auto' or set specific sizes
            # Subset the dataset within the specified region and append to list
            subset = ds.sel(lon=slice(-159.5, -157.5), lat=slice(27.5, 26))
            # Append the subset to the list of datasets
            combined_datasets.append(subset)

        # Concatenate all subsets along the 'dataset' dimension
        combined_dataset = xr.concat(combined_datasets, dim='dataset')

        # Calculate the mean Rrs value across lon and lat for each dataset
        average_per_dataset = combined_dataset.mean(dim=['lon', 'lat'])

        # Extract wavelengths and Rrs values at once to avoid repeated computation
        wavelengths = average_per_dataset['wavelength'].values
        rrs_values = average_per_dataset['Rrs'].compute()  # Trigger computation for all datasets

    return wavelengths, rrs_values

# Process the data
wavelengths, rrs_values = process(results)

# Create y-coordinates for each dataset
y_indices = np.arange(rrs_values.shape[0])  # Create an array of dataset indices

# Create a function to plot the 3D graph
def plot_3d_graph(wavelengths, y_indices, rrs_values):
    # Create a new figure
    fig = plt.figure()
    # Add a 3D subplot
    ax = fig.add_subplot(111, projection='3d')

    # Plot in 3D space using a single color (e.g., slategray)
    for dataset_index in range(rrs_values.shape[0]):
        ax.plot(wavelengths, np.full_like(wavelengths, y_indices[dataset_index]), rrs_values[dataset_index], color='slategray')

    # Set axis labels
    ax.set_xlabel('Wavelength')
    ax.set_ylabel(f'Days since {selected_dates[0].strftime("%Y-%m-%d")}')
    ax.set_zlabel('Rrs')

    # Rotate the plot 45 degrees along the Y-axis
    ax.view_init(elev=35, azim=-60)

    # Return the figure object to use in Streamlit
    return fig

# Plot the 3D graph
fig = plot_3d_graph(wavelengths, y_indices, rrs_values)
# Show the plot in Streamlit
st.pyplot(fig)
st.write('---')

# create columns for hyperspectral plot for comparison between bloom and non-bloom days
st.markdown("<h1 style='text-align: center;'>Bloom vs. No Bloom</h1>", unsafe_allow_html=True)
image_spectra = Image.open('images/spectra_range.png')
st.image(image_spectra, use_column_width=True)
col1a, col1b = st.columns([15, 15])

with col1a:
    st.markdown("<h5 style='text-align: center;'>Algal Bloom: August 16th, 2024</h5>", unsafe_allow_html=True)

    st.markdown("<h6 style='text-align: center;'>Hyperspectral Data</h6>", unsafe_allow_html=True)
    image_bloom = Image.open('images/bloom.png')
    st.image(image_bloom, use_column_width=True)
    st.markdown("<h6 style='text-align: center;'>Chlorophyl Data</h6>", unsafe_allow_html=True)
    image_chl_bloom = Image.open('images/chl_bloom.png')
    st.image(image_chl_bloom, use_column_width=True)

with col1b:
    st.markdown("<h5 style='text-align: center;'>Non Algal Bloom: July 19th, 2024</h5>", unsafe_allow_html=True)

    st.markdown("<h6 style='text-align: center;'>Hyperspectral Data</h6>", unsafe_allow_html=True)
    image_nobloom = Image.open('images/nobloom.png')
    st.image(image_nobloom, use_column_width=True)
    st.markdown("<h6 style='text-align: center;'>Chlorophyl Data</h6>", unsafe_allow_html=True)
    image_chl_nobloom = Image.open('images/chl_nobloom.png')
    st.image(image_chl_nobloom, use_column_width=True)

# commenting out code that runs chlorophyll plot to use screenshots instead for sake of time left on project
# Create a function to process and visualize the chlorophyll-a data
# def process_and_viz_chl(granule_chl):
#         # Use dask for lazy loading
#         file = earthaccess.open(granule_chl)
#         ds = xr.open_dataset(file[0], engine='h5netcdf')

#         # Subset the dataset within the specified region
#         subset = ds.sel(lon=slice(-159.5, -157.5), lat=slice(27.5, 26))
#         chla = subset["chlor_a"]

#         # Define the colors: dodgerblue to white to forest green
#         colors = ['#0A548E', 'white', 'forestgreen']

#         # Create the custom colormap
#         custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', colors)

#         # Set the figure size to [12, 20]
#         fig1 = plt.figure(figsize=(12, 20))

#         # Plot the chlorophyll-a concentration using the custom colormap, but without a colorbar
#         artist = chla.plot(cmap=custom_cmap, vmax=0.3, add_colorbar=False)

#         # Set the aspect ratio to be equal
#         plt.gca().set_aspect("equal")

#         # Add a custom, smaller colorbar
#         cbar = plt.colorbar(artist, ax=plt.gca(), aspect=10, pad=0.02,  shrink=0.4)
#         cbar.ax.tick_params(labelsize=10)  # Optional: adjust tick label size
#         cbar.ax.set_ylabel('Chlorophyll concentration\n OCI Algorithm (mg/m^3)', fontsize=12)
#         return fig1

# with col1a:
#     # Make Chlorophyll map
#     # Search for chlorophyll data
#     results_chl = earthaccess.search_data(
#         short_name="PACE_OCI_L3M_CHL_NRT",
#         granule_name="PACE_OCI.20240808.L3m.DAY.CHL.V2_0.chlor_a.4km.NRT.nc",
#     )
#     # Process and visualize the chlorophyll-a data
#     fig1 = process_and_viz_chl(results_chl)

#     st.pyplot(fig1)