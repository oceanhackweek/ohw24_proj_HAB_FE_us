import streamlit as st
from PIL import Image

st.title("Contributing Members")
st.write('---')

st.markdown("## Data Teams")
st.write("""
    - Team 1
        - Phil - PhD Candidate at the University of Southern California who studies the biogeochemistry of trace metals in the oceans and their influence on phytoplankton.
        - Farley - Works in Marine Optics & Remote Sensing at Bigelow Labs.
        - Ben - PhD Student at UMaine using oceanographic models to understand environmental impacts of floating offshore wind.
    - PACE vs Sentinel Data Team
        - Ian
        - Rafael
    - Genus Distribution Validation
         - Gulce - Post doc researcher at the Cooperative Institute for Climate, Ocean, and Ecosystem Studies

""")
st.markdown("## Application Development Team")
st.write("""
    - Adelle - Web Developer working on user-facing applications on the Ocean Data Products Team at the Gulf of Maine Research Institute
    - Adam - Quantitative research associate in the Integrated Systems Ecology Lab with the Gulf of Maine Research Institute.
    - Kasandra - Environmental Data Scientist at Axiom Data Science with over 3 years of experience working on data integration, visualization, and analysis, as well as introductory software development.
""")
st.markdown("## Team Mentor")
st.write("""
    - Eli Holmes
""")

image = Image.open('images/file.png')
st.image(image)