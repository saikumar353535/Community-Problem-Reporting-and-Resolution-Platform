
import streamlit as st

from database import init_db
from auth.authentication import register_user, login_user

# Page configuration
st.set_page_config(
    page_title="CommunityConnect",
    page_icon="🏘️",
    layout="centered"
)

# Initialize database
init_db()

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# Application heading
st.title("🏘️ CommunityConnect")
st.subheader("Your Voice. Your Community. Your Change.")
st.write("Report community problems and help make your neighbourhood better.")

st.divider()


# Logged-in citizen home page
if st.session_state.logged_in:

    user = st.session_state.user

    st.success(f"Welcome, {user['name']}!")

    st.write("You are successfully logged in.")
    st.info(f"Registered email: {user['email']}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()


# Registration and login pages
else:

    register_tab, login_tab = st.tabs(
        ["📝 Register", "🔐 Login"]
    )

    # Registration
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

                if password != confirm_password:
                    st.error("Passwords do not match.")

                else:
                    success, message = register_user(
                        name,
                        email,
                        password
                    )

                    if success:
                        st.success(message)
                        st.info("Please go to the Login tab.")

                    else:
                        st.error(message)

    # Login
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

                    st.success("Login successful!")
                    st.rerun()

                else:
                    st.error("Invalid email or password.")


st.divider()

st.caption("CommunityConnect | Building Better Communities Together")
