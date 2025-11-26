# state_manager.py
import streamlit as st

def init_state():
    if "users" not in st.session_state:
        st.session_state.users = {
            "admin": {"password": "admin123", "type": "admin"},
            "team1": {"password": "t1pass", "type": "team"},
            "team2": {"password": "t2pass", "type": "team"},
        }
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "team_data" not in st.session_state:
        st.session_state.team_data = {
            "team1": {"credits": 100, "pipeline": [], "score": 0},
            "team2": {"credits": 100, "pipeline": [], "score": 0},
        }
    if "current_round" not in st.session_state:
        st.session_state.current_round = 1
    if "bids" not in st.session_state:
        st.session_state.bids = {}
