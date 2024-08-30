import streamlit as st
import datetime

st.title("Genus Distribution Validation")
st.subheader("description goes here")
st.subheader("Contributing members: Gulce")
st.write('---')



with st.sidebar:
    st.write("----")
    select_dates = st.date_input(
        "Select a date to compare",
        value = datetime.date(2024, 7, 1),
        min_value = datetime.date(2024, 7, 1),
        max_value = datetime.date(2024, 8, 25),
        format = "YYYY-MM-DD",
        label_visibility = "visible"
    )