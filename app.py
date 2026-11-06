
import streamlit as st

from database import init_db
from auth.authentication import register_user, login_user
from auth.citizen_home import show_citizen_home
from auth.profile import show_profile


# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="CommunityConnect",
    page_icon="🏘️",
    layout="centered"
)


# ----------------------------------
# INITIALIZE DATABASE
# ----------------------------------

init_db()


# ----------------------------------
# SESSION STATE
# ----------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "home"


# ----------------------------------
# APPLICATION HEADER
# ----------------------------------

st.title("🏘️ CommunityConnect")

st.caption("Your Voice. Your Community. Your Change.")

st.write(
    "Report community problems and help "
    "make your neighbourhood better."
)

st.divider()


# ----------------------------------
# LOGGED-IN CITIZEN SECTION
# ----------------------------------

if st.session_state.logged_in:

    current_user = st.session_state.user

    if st.session_state.page == "profile":

        show_profile(current_user)

    else:

        # Dashboard is called only ONCE
        show_citizen_home(current_user)


# ----------------------------------
# REGISTRATION AND LOGIN SECTION
# ----------------------------------

else:

    register_tab, login_tab = st.tabs(
        ["📝 Register", "🔐 Login"]
    )

    # ----------------------------------
    # CITIZEN REGISTRATION
    # ----------------------------------

    with register_tab:

        st.subheader("Create Your Citizen Account")

        with st.form("registration_form"):

            name = st.text_input("Full Name")

            email = st.text_input("Email Address")

            password = st.text_input(
                "Create Password",
                type="password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            register_button = st.form_submit_button(
                "Create Account",
                use_container_width=True
            )

            if register_button:

                if not name.strip() or not email.strip():
                    st.error("Please enter your name and email.")

                elif password != confirm_password:
                    st.error("Passwords do not match.")

                else:

                    success, message = register_user(
                        name,
                        email,
                        password
                    )

                    if success:

                        st.success(message)

                        st.info(
                            "Your account has been created. "
                            "Please log in using the Login tab."
                        )

                    else:

                        st.error(message)

    # ----------------------------------
    # CITIZEN LOGIN
    # ----------------------------------

    with login_tab:

        st.subheader("Citizen Login")

        with st.form("login_form"):

            login_email = st.text_input("Email Address")

            login_password = st.text_input(
                "Password",
                type="password"
            )

            login_button = st.form_submit_button(
                "Login",
                use_container_width=True
            )

            if login_button:

                success, user = login_user(
                    login_email,
                    login_password
                )

                if success:

                    st.session_state.logged_in = True

                    st.session_state.user = user

                    st.session_state.page = "home"

                    st.rerun()

                else:

                    st.error(
                        "Invalid email or password. "
                        "Please try again."
                    )


# ----------------------------------
# FOOTER
# ----------------------------------

st.divider()

st.caption(
    "CommunityConnect | Building Better Communities Together"
)
