# pages/7_Admin.py
import streamlit as st
from state_manager import init_state
from auction_manager import resolve_round

init_state()
user = st.session_state.current_user

if user is None or st.session_state.users[user]["type"] != "admin":
    st.warning("Admin access only.")
else:
    st.title("Admin Panel")
    st.write(f"Current Auction Round: {st.session_state.current_round}")

    st.write("Team Overview:")
    for team, data in st.session_state.team_data.items():
        st.write(f"- {team}: Credits {data['credits']}, Modules: {', '.join(data['pipeline'])}")

    st.write("---")
    st.subheader("Resolve Auction Round")
    if st.button("Resolve Current Round"):
        result = resolve_round()
        if result:
            team, module, bid = result
            st.success(f"{team} won {module} with {bid} credits!")
        else:
            st.info("No bids placed yet.")
