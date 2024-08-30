import streamlit as st

st.title('OceanHackWeek: Streamlit Tutorial')
st.subheader('You can also add additional pages to your Streamlit app!')
st.write('---')
st.write('To add additional pages to your Streamlit app, you would create a `pages` folder in the same folder as your main page and add a separate Python file to that folder.')
st.code('''
        main_directory/
            application.py
            pages/
                1_Example_Page_One.py
                2_Example_Page_Two.py
                3_Example_Page_Three.py
        ''')
st.write("Additional page titles will displayed in the sidebar based on what the file name is.")

st.write("----")

st.write('This is what this page (`Additional Pages`) looks in code:')
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
