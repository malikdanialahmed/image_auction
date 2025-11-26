import streamlit as st

st.title("Imaging Auction - Test App")
st.write("If you see this, Streamlit is working!")
st.title("Title")
st.write("Some text")
if st.button("Click me"):
    st.write("You clicked the button!")
tab1, tab2 = st.tabs(["Team 1", "Team 2"])
if "credits" not in st.session_state:
    st.session_state["credits"] = 100

import streamlit as st

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Setup", "Auction", "Results"])

if page == "Home":
    st.title("Welcome to Imaging Auction")
    st.write("Build a medical imaging pipeline under limited credits!")

elif page == "Setup":
    st.title("Team Setup")
    team1 = st.text_input("Team 1 Name")
    team2 = st.text_input("Team 2 Name")

elif page == "Auction":
    st.title("Auction Page")
    st.write("Modules will go here")

elif page == "Results":
    st.title("Final Results")
