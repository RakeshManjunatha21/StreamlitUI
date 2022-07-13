#Import modules
import streamlit as st
#import pandas as pd
#import pickle as pkle

def login_func():
    """
    Function to Authenticate login and creation of new account
    """
    st.title("Serverlog Analytics")
    login_dropdown = ['Login','SignUp']
    choice = st.selectbox('',login_dropdown)
    if choice == 'Login':
        st.subheader('Login')
        username = st.text_input("User Name")
        password = st.text_input('Password',type='password')
        if st.checkbox('Submit'):
            st.success('Logged In as {}'.format(username))
            return "Success"

    elif choice == 'SignUp':
        st.subheader('Create New Account')