import streamlit as st

st.title('OceanHackWeek: Streamlit Tutorial')
st.subheader('You can also add additional pages to your Streamlit app!')
st.write('---')
st.write('To add additional pages to your Streamlit app, you would create a `pages` folder in the same folder as your main page and add a separate Python file to that folder.')
st.code('''
        main_directory/
            application.py
            pages/
                page1.py
                page2.py
                page3.py
        ''')

st.write('Code example for `Additional_Pages.py`:')
st.code('''
        import streamlit as st

        st.title('OceanHackWeek: Streamlit Tutorial')
        st.subheader('You can also add additional pages to your Streamlit app!')
        st.write('---')
        st.write('To add additional pages to your Streamlit app, you would create a `pages` folder in the same folder as your main page and add a separate Python file to that folder.')
        st.code("""
                main_directory/
                    application.py
                    pages/
                        page1.py
                        page2.py
                        page3.py"
                """)
        ''')
