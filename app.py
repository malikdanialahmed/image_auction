# app.py
import streamlit as st

st.title("Welcome to Imaging Auction")
st.write("Use the sidebar to navigate between pages.")

# Example at top of 1_Login.py
from state_manager import init_state
init_state()
