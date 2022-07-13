#Import Modules
import streamlit as st
import pandas as pd

# @st.cache()
# def load_file():
#     serverlog_df = st.file_uploader("Upload Serverlog Data", type={"csv"})
#     return serverlog_df

def selected_page_func():
    """
    Function to upload files and connect to database
    """
    st.title('Upload')
    import_dropdown = ['Upload Serverlog Data','Connect to Database']
    choice = st.selectbox('Choose',import_dropdown)
    
    if choice == 'Upload Serverlog Data':
        # serverlog_df = load_file()
        serverlog_df = st.file_uploader("Upload Serverlog Data", type={"csv"})
        if serverlog_df is not None:
            server_data_nd = pd.read_csv(serverlog_df)
            #server_data_nd.to_csv("server_data.csv")
            st.success("File uploaded successfully")
            view_sample_data = server_data_nd.head(10)
            st.write(view_sample_data)