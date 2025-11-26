# auction_manager.py
import streamlit as st

def place_bid(team, module, bid_amount):
    if bid_amount <= st.session_state.team_data[team]["credits"]:
        st.session_state.bids[team] = {"module": module, "bid": bid_amount}
        return True
    return False

def resolve_round():
    if not st.session_state.bids:
        return None
    winner = max(st.session_state.bids.items(), key=lambda x: x[1]["bid"])
    team = winner[0]
    module = winner[1]["module"]
    bid = winner[1]["bid"]

    st.session_state.team_data[team]["credits"] -= bid
    st.session_state.team_data[team]["pipeline"].append(module)
    st.session_state.bids = {}
    st.session_state.current_round += 1
    return team, module, bid
