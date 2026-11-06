
import streamlit as st


def show_profile(user):

    st.title("👤 My Citizen Profile")

    st.write("View your registered account information.")

    st.divider()

    st.subheader("Personal Information")

    st.text_input(
        "Full Name",
        value=user["name"],
        disabled=True
    )

    st.text_input(
        "Email Address",
        value=user["email"],
        disabled=True
    )

    st.info(
        "Your account information is currently displayed "
        "in read-only mode."
    )

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "home"
        st.rerun()
