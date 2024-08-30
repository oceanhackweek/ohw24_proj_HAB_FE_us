import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# Additional Resources")
st.sidebar.header("Additional Resources")
st.write("""
This page provides you with additional resources that you may find useful for further exploration and learning.
Feel free to browse through the various categories of resources listed below.
""")

st.subheader("About PACE")
st.write("""
    - [About PACE](https://pace.oceansciences.org/about.htm)
    - [About PACE Data](https://pace.oceansciences.org/access_pace_data.htm)
""")
# progress_bar = st.sidebar.progress(0)
# status_text = st.sidebar.empty()
# last_rows = np.random.randn(1, 1)
# chart = st.line_chart(last_rows)

# for i in range(1, 101):
#     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#     status_text.text("%i%% Complete" % i)
#     chart.add_rows(new_rows)
#     progress_bar.progress(i)
#     last_rows = new_rows
#     time.sleep(0.05)

# progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
# st.button("Re-run")