import streamlit as st
import hashlib
import json
from typing import Dict

# ----------------------------
# Helper functions
# ----------------------------
def hash_password(password: str) -> str:
    """Return SHA-256 hash of the password."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_app_state():
    """Initialize app-level session state (users, current_user, etc.)."""
    if "users" not in st.session_state:
        # default user store structure:
        # username -> { "password": <hashed>, "type": "admin"|"team", "team_name": str, "credits": int, "pipeline": [] }
        st.session_state.users = {
            "admin": {
                "password": hash_password("admin123"),
                "type": "admin",
                "team_name": "Administrators",
                "credits": 0,
                "pipeline": [],
            }
        }
    if "current_user" not in st.session_state:
        st.session_state.current_user = None  # username string or None
    if "login_message" not in st.session_state:
        st.session_state.login_message = ""

def create_team_user(username: str, password: str, team_name: str, credits: int = 100) -> bool:
    """Create a new team user. Returns False if username exists."""
    username = username.strip().lower()
    if username in st.session_state.users:
        return False
    st.session_state.users[username] = {
        "password": hash_password(password),
        "type": "team",
        "team_name": team_name,
        "credits": credits,
        "pipeline": [],
    }
    return True

def authenticate(username: str, password: str) -> bool:
    username = username.strip().lower()
    user = st.session_state.users.get(username)
    if not user:
        return False
    return user["password"] == hash_password(password)

def logout():
    st.session_state.current_user = None
    st.session_state.login_message = "Logged out."

# Optional persistence helpers (uncomment to use local JSON persistence)
def save_users_to_file(path="users_store.json"):
    with open(path, "w") as f:
        json.dump(st.session_state.users, f)

def load_users_from_file(path="users_store.json"):
    try:
        with open(path, "r") as f:
            st.session_state.users = json.load(f)
    except FileNotFoundError:
        pass

# ----------------------------
# Initialize
# ----------------------------
st.set_page_config(page_title="Imaging Auction — Login", layout="wide")
init_app_state()
# load_users_from_file()  # optional: uncomment to load from disk at startup

# ----------------------------
# UI: Sidebar navigation
# ----------------------------
st.sidebar.title("Navigation")
if st.session_state.current_user:
    user = st.session_state.users[st.session_state.current_user]
    st.sidebar.markdown(f"**Logged in as:** `{st.session_state.current_user}`  ")
    st.sidebar.markdown(f"**Role:** {user['type']}  ")
    if user["type"] == "team":
        st.sidebar.markdown(f"**Team name:** {user['team_name']}  ")
        st.sidebar.markdown(f"**Credits:** {user['credits']}  ")
    if st.sidebar.button("Logout"):
        logout()
        st.experimental_rerun()
else:
    st.sidebar.write("You are not logged in")

page = st.sidebar.selectbox("Go to", ["Login", "Sign Up", "Who am I?"])

# ----------------------------
# Page: Login
# ----------------------------
if page == "Login":
    st.title("Login — Imaging Auction")
    st.info("Use the default admin: `admin` / `admin123` to test admin features.")
    col1, col2 = st.columns([2, 1])
    with col1:
        username = st.text_input("Username").strip().lower()
        password = st.text_input("Password", type="password")
    with col2:
        st.write(" ")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.current_user = username
                st.session_state.login_message = f"Logged in as {username}"
                st.success(st.session_state.login_message)
                st.experimental_rerun()
            else:
                st.error("Invalid credentials. Try again or Sign Up.")

    if st.session_state.login_message:
        st.write(st.session_state.login_message)

# ----------------------------
# Page: Sign Up
# ----------------------------
elif page == "Sign Up":
    st.title("Sign Up — Create a Team Account")
    st.write("Create a team account to participate in auctions. Your account is stored in memory (session).")
    new_user = st.text_input("Choose a username (letters, numbers, dash/underscore).").strip().lower()
    new_team = st.text_input("Team/display name (what others see)").strip()
    new_pass = st.text_input("Choose a password", type="password")
    confirm_pass = st.text_input("Confirm password", type="password")

    if st.button("Create Team Account"):
        if not new_user or not new_pass or not new_team:
            st.error("Please fill all fields.")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match.")
        elif new_user in st.session_state.users:
            st.error("Username already exists. Choose another username.")
        else:
            created = create_team_user(new_user, new_pass, new_team, credits=100)
            if created:
                st.success(f"Team `{new_team}` created! You can now log in with username `{new_user}`.")
                st.info("Note: This user store is in-memory while the app runs. If you restart the app, data will reset unless you add persistence.")
                # save_users_to_file()  # optional: uncomment to persist immediately
            else:
                st.error("Could not create user (maybe username exists).")

# ----------------------------
# Page: Who am I? (Quick debug / info)
# ----------------------------
elif page == "Who am I?":
    st.title("Session Info")
    if st.session_state.current_user:
        user = st.session_state.users[st.session_state.current_user]
        st.write("### Current user info:")
        st.json({k: v for k, v in user.items() if k != "password"})
    else:
        st.write("Not logged in.")
    st.write("---")
    st.write("### All users (for debugging / admin):")
    for u, info in st.session_state.users.items():
        safe_info = {k: v for k, v in info.items() if k != "password"}
        st.write(f"- `{u}` → {safe_info}")

# ----------------------------
# Admin quick user-management UI (render only if admin logged in)
# ----------------------------
if st.session_state.current_user:
    current = st.session_state.users[st.session_state.current_user]
    if current["type"] == "admin":
        st.markdown("---")
        st.header("Admin — User Management (quick)")
        st.write("Create a team account from here, or inspect existing accounts.")
        with st.form("admin_create_team"):
            c_username = st.text_input("New username (team account)").strip().lower()
            c_teamname = st.text_input("Team/display name").strip()
            c_password = st.text_input("Initial password", type="password")
            submitted = st.form_submit_button("Create team account")
            if submitted:
                if not c_username or not c_password or not c_teamname:
                    st.error("Please fill all fields.")
                elif c_username in st.session_state.users:
                    st.error("Username already exists.")
                else:
                    create_team_user(c_username, c_password, c_teamname, credits=100)
                    st.success(f"Created team `{c_teamname}` with username `{c_username}`.")
                    # save_users_to_file()  # optional: persist
        st.write("#### Registered users:")
        for u, info in st.session_state.users.items():
            st.write(f"- **{u}** ({info['type']}) — Team: {info['team_name']} — Credits: {info.get('credits', 'N/A')}")

# ----------------------------
# Quick placeholders to continue building (only visible after login)
# ----------------------------
if st.session_state.current_user:
    u = st.session_state.current_user
    user = st.session_state.users[u]
    if user["type"] == "team":
        st.sidebar.markdown("---")
        if st.sidebar.button("Open Team Dashboard (placeholder)"):
            st.experimental_set_query_params(page="team_dashboard")
            st.success("Team Dashboard will be implemented next. (This is a placeholder.)")
    elif user["type"] == "admin":
        st.sidebar.markdown("---")
        if st.sidebar.button("Open Admin Panel (placeholder)"):
            st.experimental_set_query_params(page="admin_panel")
            st.success("Admin Panel will be implemented next. (This is a placeholder.)")

# End of file
