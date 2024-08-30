import streamlit as st
import datetime
from PIL import Image


st.title("Genus Distribution Validation")
st.markdown("<h4>Long Island Case Study: Plotting surface reflectance for a region off Long Island that we know has a long-running census of plankton genus. We display the spectra over a month, pick out an anomaly, and then gather and plot the corresponding plankton distribution.</h4>", unsafe_allow_html=True)
st.markdown("<h4>Contributing members: Gulce</h4>", unsafe_allow_html=True)
st.write('---')



with st.sidebar:
    st.write("----")
    select_dates = st.date_input(
        "Select a date to compare",
        value = datetime.date(2024, 7, 7),
        min_value = datetime.date(2024, 7, 1),
        max_value = datetime.date(2024, 8, 25),
        format = "YYYY-MM-DD",
        label_visibility = "visible"
    )

col1, col2 = st.columns([30, 30])

st.markdown("<h5 style='text-align: center;'>Genus distribution for July 7th, 2024</h5>", unsafe_allow_html=True)
image_genus_dist = Image.open("app/images/Genus-distribution.png")
st.image(image_genus_dist, use_column_width=True)

st.markdown("<h5 style='text-align: center;'>Hyperspectral Data for July 7th, 2024</h5>", unsafe_allow_html=True)
image_genus_dist = Image.open("app/images/Genus-dist-spectra.png")
st.image(image_genus_dist, use_column_width=True)
