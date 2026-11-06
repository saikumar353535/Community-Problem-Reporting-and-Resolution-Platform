
import streamlit as st

from auth.profile import show_profile


def show_citizen_home(user):

    # Profile page
    if st.session_state.get("page") == "profile":
        show_profile(user)
        return

    st.title("🏘️ Citizen Dashboard")

    st.subheader(f"Welcome, {user['name']}! 👋")

    st.write(
        "Together, we can make our neighbourhood better."
    )

    st.divider()

    st.subheader("What would you like to do today?")

    col1, col2 = st.columns(2)

    with col1:
        st.info("📢 Report a Problem")
        st.write("Report community issues.")

        if st.button("Report an Issue", use_container_width=True):
            st.session_state.page = "report"
            st.rerun()

    with col2:
        st.info("📋 My Complaints")
        st.write("Track your submitted complaints.")

        if st.button("View My Complaints", use_container_width=True):
            st.session_state.page = "my_complaints"
            st.rerun()

    st.divider()

    st.subheader("👤 My Account")

    if st.button("View My Profile", use_container_width=True):
        st.session_state.page = "profile"
        st.rerun()

    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = "home"
        st.rerun()
