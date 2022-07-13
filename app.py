import streamlit as st

import login
import pages

PAGES = {
    "Login Page": login,
    "Page Index": pages 
}

login_page = PAGES["Login Page"]
val = login_page.login_func()

if val == "Success":
    page_index = PAGES["Page Index"]
    page_index.page_index_func()