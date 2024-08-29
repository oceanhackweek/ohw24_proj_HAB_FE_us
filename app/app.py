import streamlit as st
import dask
import earthaccess
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import cmocean
import coiled
from matplotlib.colors import LinearSegmentedColormap


st.title('OceanHackWeek: Bloom and Gloom Dashboard')
st.subheader('Application to showcase Algal Bloom Hyperspectral Data!')
st.write('---')

with st.sidebar:
    st.header('Project Overview')
    st.subheader('Participants')
    st.write('Data Team: Phil, Farley, Ben')
    st.write('App Team: Adelle, Adam, Kasandra')
    st.subheader('Source Data')
    st.write('PACE OCI Level-3 Global Mapped Remote-Sensing Reflectance (RRS) - NRT Data, version 2.0, NASA Earthdata')
    st.write('---')
    ### TODO - finish this
    add_selectbox = st.sidebar.selectbox(
        "Example Select Box",
        ("opt1", "opt2", "opt3")
    )


# dask setup
# run the following in terminal before spinning up the app
# coiled login --token 48c0361f39984d7b8bab62f3252a5d7e-e6c38c5e8b15f967b104cf58ee289f4066ccd330

cluster = coiled.Cluster(
    region="us-west-2",
    arm=True,   # run on ARM to save energy & cost
    worker_vm_types=["t4g.small"],  # cheap, small ARM instances, 2cpus, 2GB RAM
    worker_options={'nthreads':2},
    n_workers=30,
    wait_for_workers=False,
    compute_purchase_option="spot_with_fallback",
    name='coawst',   # Dask cluster name
    software='esip-pangeo-arm',  # Conda environment name
    workspace='esip-lab',
    timeout=180   # leave cluster running for 3 min in case we want to use it again
)

client = cluster.get_client()

# the following code was created by the data team, all credit goes to them

# .netrc file is required for authentication (Please fill out with your earthdata login credentials)
auth = earthaccess.login()
# are we authenticated?
if auth.authenticated:
    st.write("Data Access Authenticated!")
if not auth.authenticated:
    # ask for credentials and persist them in a .netrc file
    raise ValueError("Authentication failed. Please check your .netrc file.")

tspan = ("2024-07-01", "2024-08-25")
bbox = (-170, 23, -140, 33)
clouds = (0, 50)

results = earthaccess.search_data(
    short_name="PACE_OCI_L3M_RRS_NRT",
    temporal=tspan,
    bounding_box=bbox,
    granule_name="PACE_OCI.20240701.L3m.DAY.RRS.V2_0.Rrs.0p1deg.NRT.nc",
)

paths = earthaccess.open(results)