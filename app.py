import streamlit as st

from src.auth import authenticate
from src.database.initialize import initialize_database

from src.ui.dashboard import show_dashboard
from src.ui.patient_registration import show_patient_registration
from src.ui.patient_list import show_patient_list
from src.ui.consultation import show_consultation
from src.ui.consultation_history import show_consultation_history
from src.ui.model_performance import show_model_performance


# ---------------------------------------------------------
# Initial Setup
# ---------------------------------------------------------

st.set_page_config(
    page_title="RuralCareAI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_database()


# ---------------------------------------------------------
# Session State
# ---------------------------------------------------------

DEFAULT_SESSION = {
    "logged_in": False,
    "user": None,
    "role": None,
    "current_page": "Dashboard",
}

for key, value in DEFAULT_SESSION.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------------------------------------------------
# Login Screen
# ---------------------------------------------------------

if not st.session_state.logged_in:

    st.title("🏥 RuralCareAI")
    st.subheader("AI-Based Rural Healthcare Triage Assistant")

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown("## Login")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password",
        )

        if st.button(
            "Login",
            use_container_width=True,
        ):

            user = authenticate(username, password)

            if user:

                st.session_state.logged_in = True
                st.session_state.user = user.full_name
                st.session_state.role = user.role

                st.rerun()

            else:

                st.error("Invalid username or password")

    st.stop()


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.title("🏥 RuralCareAI")

    st.write(f"**User:** {st.session_state.user}")
    st.write(f"**Role:** {st.session_state.role}")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Patient Registration",
            "Patient List",
            "Consultation",
            "Consultation History",
            "Model Performance"
        ],
        index=[
            "Dashboard",
            "Patient Registration",
            "Patient List",
            "Consultation",
            "Consultation History",
            "Model Performance"
        ].index(st.session_state.current_page),
    )

    st.session_state.current_page = page

    st.divider()

    if st.button(
        "Logout",
        use_container_width=True,
    ):

        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
        st.session_state.current_page = "Dashboard"

        st.rerun()


# ---------------------------------------------------------
# Main Screen
# ---------------------------------------------------------

if page == "Dashboard":
    show_dashboard()

elif page == "Patient Registration":
    show_patient_registration()

elif page == "Patient List":
    show_patient_list()

elif page == "Consultation":
    show_consultation()

elif page == "Consultation History":
    show_consultation_history()

elif page == "Model Performance":
    show_model_performance()