# app.py
import streamlit as st
from state_manager import init_state

init_state()

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Login", "Team Dashboard", "Module Store", "Bidding", "Pipeline", "Results", "Admin"])
