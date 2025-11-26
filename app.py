import streamlit as st

# ----------------------------
# INITIAL SETUP
# ----------------------------

# Session state initialization
if "team_name" not in st.session_state:
    st.session_state.team_name = ""
if "credits" not in st.session_state:
    st.session_state.credits = 100
if "pipeline" not in st.session_state:
    st.session_state.pipeline = []

# ----------------------------
# MODULE CATALOG
# ----------------------------
modules = {
    "Z-Score Norm": {
        "cost": 6,
        "description": "+0.03 with any classifier (essential for DL)"
    },
    "N4 Bias-Field": {
        "cost": 18,
        "description": "+0.03 if Registration present; +0.01 extra if U-Net"
    },
    "NLM Denoise": {
        "cost": 22,
        "description": "+0.04 with GLCM; +0.01 generic"
    },
    "CLAHE": {
        "cost": 8,
        "description": "+0.02 with Otsu; -0.01 with U-Net"
    },
    "Rigid + NCC": {
        "cost": 20,
        "description": "+0.02 mono-modal"
    },
    "Affine + MI": {
        "cost": 30,
        "description": "+0.05 multi-modal; +0.02 mono-modal"
    },
    "Deformable B-spline": {
        "cost": 28,
        "description": "+0.03 with EM/U-Net; -0.02 without preprocessing"
    },
    "GLCM": {
        "cost": 12,
        "description": "+0.06 with NLM; -0.03 without denoise"
    },
    "LBP": {
        "cost": 10,
        "description": "+0.03 with K-means/EM"
    },
    "Otsu": {
        "cost": 5,
        "description": "+0.02 with CLAHE"
    },
    "K-means": {
        "cost": 8,
        "description": "+0.04 with MRF"
    },
    "EM (GMM)": {
        "cost": 14,
        "description": "+0.02 vs K-means; +0.02 with MRF"
    },
    "Random Forest": {
        "cost": 20,
        "description": "+0.05 with GLCM/LBP; +0.02 with Norm"
    },
    "U-Net": {
        "cost": 55,
        "description": "+0.10; -0.05 without Z-Score; +0.02 with N4"
    },
    "MRF/CRF": {
        "cost": 20,
        "description": "+0.05 with K-means/EM; +0.01 with U-Net"
    },
}

# ----------------------------
# UI NAVIGATION
# ----------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Team Setup", "Module Store", "Your Pipeline"])

# ----------------------------
# PAGE 1 — TEAM SETUP
# ----------------------------
if page == "Team Setup":
    st.title("Create Your Team")

    st.session_state.team_name = st.text_input("Enter team name:")

    st.write("Starting credits: **100**")

    if st.session_state.team_name:
        st.success(f"Team **{st.session_state.team_name}** created!")
        st.info("Go to the *Module Store* to start building your pipeline.")

# ----------------------------
# PAGE 2 — MODULE STORE (PURCHASE SYSTEM)
# ----------------------------
elif page == "Module Store":
    st.title("Available Modules")
    st.write(f"**Team:** {st.session_state.team_name}")
    st.write(f"**Credits remaining:** {st.session_state.credits}")

    for module, info in modules.items():
        st.subheader(module)
        st.write(f"Cost: **{info['cost']}** credits")
        st.write(info["description"])

        if module in st.session_state.pipeline:
            st.success("Already purchased")
        else:
            if st.session_state.credits >= info["cost"]:
                if st.button(f"Buy {module}"):
                    st.session_state.pipeline.append(module)
                    st.session_state.credits -= info["cost"]
                    st.experimental_rerun()
            else:
                st.error("Not enough credits")

        st.markdown("---")

# ----------------------------
# PAGE 3 — PIPELINE DISPLAY
# ----------------------------
elif page == "Your Pipeline":
    st.title("Your Pipeline")
    st.write(f"Team: **{st.session_state.team_name}**")

    if len(st.session_state.pipeline) == 0:
        st.warning("You haven't purchased anything yet.")
    else:
        st.write("### Selected Modules:")
        for m in st.session_state.pipeline:
            st.write(f"- {m}")

        st.write("---")
        st.write(f"**Remaining Credits:** {st.session_state.credits}")
