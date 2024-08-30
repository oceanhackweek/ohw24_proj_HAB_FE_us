# P.A.C.E.: People Accessing Cool Examples

## Collaborators
| Name                | Location   | Role                |
|---------------------|------------|---------------------|
| Adelle              | Bigelow    | Participant         |
| Adam                | Bigelow    | Participant         |
| Kasandra            | Bigelow    | Participant         |

## Project Description
The goal is to create an app that will use Streamlit to make it easy to view and explore PACE (Plankton, Aerosol, Cloud, ocean Ecosystem) data, with a focus on algal blooms. The app will let users interact with the data through simple controls like sliders and date selection, and see some updates in real time. It will be easy to use, gathering data from different sources and showing it in a clear way. We worked on building and testing the app, using Streamlit and other libraries, while making sure the data fits together well.

## Planning
* Initial idea: Create an app to help showcase PACE data
* Final idea: Create an app to help showcase the culmination of data from the three PACE data teams.
* Ideation Presentation: [Link](https://docs.google.com/presentation/d/1SR6d_zO2U5_nc25R4WQ_o4BMq0qJhAeIvwECZf4PzvU/edit#slide=id.p)
* Slack channel: ohw24_proj_hab_fe_us
* Final presentation: TBD

## Resources
* streamlit.com
* https://github.com/oceanhackweek/ohw24_proj_pace_us

## This README includes instructions on how to spin up your very own Streamlit app locally. 
#### Unfortunately, we were not able to figure out how to run this in JupyterHub

#### Instructions using conda (please note this workflow has not been extensively tested so please get assistance from someone familiar with setting up local environments)
1. Install conda/miniconda/anaconda: https://docs.anaconda.com/
There are two options:
2. In your computer's terminal
   a. `git clone repo`
   b. `conda create --name env-name`
   c. `conda activate env-name`
   d. `pip install -r requirements.txt` which can be copied from this repo and customized to include the packages you need
or 
2. In your computer's terminal
   a. `git clone repo`
   b. `conda env create -f environment.yml`
   c. `conda activate ohw-streamlit`
3. Create `streamlit.py` which you can name whatever you want
4. Add your code!
5. Run `streamlit run streamlit.py` or update to use your file name
   If you would like the app to update every time you save (this is good for debugging) run `streamlit run --server.runOnSave true streamlit.py`

#### To run this application: `streamlit run --server.runOnSave true app/app.py`
