#Import Modules
import streamlit as st

#Custom Import
import analytics
import anomalies
import upload
import prediction


def page_index_func():
    """Function for different options 
    Upload, Insites, Anomalies, Prediction
    """
    PAGES = {
        "Upload": upload,
        "Insights": analytics,
        "Anomalies": anomalies,
        "Prediction": prediction,
        
    }
    st.sidebar.title('Server Analytics')
    selection = st.sidebar.radio("", list(PAGES.keys()))
    page = PAGES[selection]
    page.selected_page_func()