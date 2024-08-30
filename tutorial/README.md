# This README includes instructions on how to spin up your very own streamlit app locally. 
### Unforunately we were not able to figure out how to run this in JupyterHub
### Instructions using conda
1. Install conda/miniconda/anaconda: https://docs.anaconda.com/
2. In your computer's terminal
   a. `git clone repo`
   b. `conda create --name env-name`
   c. `conda activate env-name`
   d. `pip install requirements.txt` which can be copied from this repo and customized to include the packages you need
3. Create `streamlit.py` which you can name whatever you want
4. Add your code!
5. Run `streamlit run streamlit.py` or update to use your file name
   If you would like the app to update every time you save (this is good for debugging) run `streamlit run --server.runOnSave true streamlit.py`
