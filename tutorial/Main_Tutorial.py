import streamlit as st
import matplotlib.pyplot as plt 
import numpy as np

st.title('OceanHackWeek: Streamlit Tutorial')
st.subheader('More information about Streamlit can be found at https://streamlit.io/')
st.write('There are many ways to customize your Streamlit app, including the use of sidebars, widgets, and more!')
st.write('---')
st.write('This is the main content of the app. You can add text, images, and more here.')
st.write('Code example for starting point:')
st.code('''
        import streamlit as st

        st.title('OceanHackWeek: Streamlit Tutorial')
        st.subheader('More information about Streamlit can be found at https://streamlit.io/')
        st.write('There are many ways to customize your Streamlit app, including the use of sidebars, widgets, and more!')
        st.write('---')
        st.write('This is the main content of the app. You can add text, images, and more here.')
        ''')

with st.sidebar:
    st.header('Look at this sidebar!')
    st.subheader('Anything you want can be added here,')
    st.write('including filters using a selectbox')
    st.selectbox(
    "Like this one!",
    ("Option 1", "Option 2", "Option 3"))
    st.write('Code example for sidebar1:')
    st.code('''
            with st.sidebar:
                st.header('Look at this sidebar!')
                st.subheader('Anything you want can be added here,')
                st.write('including filters using a selectbox')
                st.selectbox(
                "Like this one!",
                ("Option 1", "Option 2", "Option 3"))
            ''')


st.selectbox(
    "You can also add selectboxes in the main page as well!",
    ("Selection 1", "Selection 2", "Selection 3"))
st.write('Code example for selectbox2:')
st.code('''
        st.write('This is the main content of the app. You can add text, images, and more here.')
        st.selectbox(
            "You can also add selectboxes in the main page as well!",
            ("Selection 1", "Selection 2", "Selection 3"))
        ''')
st.write('Example Image:')
# add image
st.image('https://www.surfertoday.com/images/stories/oceanography.jpg', use_column_width=True)
st.write('Code example for importing images:')
st.code('''
        st.write('Example Image:')
        # add image
        st.image('https://www.surfertoday.com/images/stories/oceanography.jpg', use_column_width=True)
        ''')
st.write('Example Plot:')
# add simple plot=
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y)
st.pyplot(plt)
st.write('Code example for adding a plot:')
st.code('''
        st.write('Example Plot:')
        # add simple plot=
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        plt.plot(x, y)
        st.pyplot(plt)
        ''')