import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

import pandas as pd
from erddapy import ERDDAP

st.title('Test App for OHW')

DATE_COLUMN = "date/time"
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text("loading data...")

data = load_data(100)

data_load_state.text("Done! (using st.cache_data)")

st.subheader('Raw data')
st.write(data)

st.subheader('Number of pickups by hour')

hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)
