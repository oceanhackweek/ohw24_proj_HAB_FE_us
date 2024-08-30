import streamlit as st
import datetime

st.title("Comparing PACE and Sentinel Data")
st.markdown("<h4>description goes here</h4>", unsafe_allow_html=True)
st.markdown("<h4>Contributing members: Ian and Rafael</h4>", unsafe_allow_html=True)
st.write('---')

# screenshot of 0-1 visualized and explanations
# screenshot of anything else they want

with st.sidebar:
    st.header("PACE vs Sentinel Data")
    st.write("----")
    select_dates = st.date_input(
        "Select a date to compare",
        value = datetime.date(2024, 7, 1),
        min_value = datetime.date(2024, 7, 1),
        max_value = datetime.date(2024, 8, 25),
        format = "YYYY-MM-DD",
        label_visibility = "visible"
    )