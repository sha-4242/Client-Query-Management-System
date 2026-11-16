
import streamlit as st
from database.db import create_tables
from utils.auth import register_user, login_user

# Create database tables
create_tables()

st.set_page_config(
    page_title="Client Query Management System",
    page_icon="📩",
    layout="wide"
)

st.title("📩 Client Query Management System")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e0e7ff, #f5f3ff, #ede9fe);
}

h1 {
    color: #4338ca !important;
    font-weight: 800;
    text-align: center;
}

h2, h3 {
    color: #5b21b6 !important;
}

.stButton > button {
    background: linear-gradient(90deg, #4f46e5, #9333ea);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
}

.stButton > button:hover {
    background: #3730a3;
    color: white;
    border: none;
}

</style>
""", unsafe_allow_html=True)


# Session management
if "user" not in st.session_state:
    st.session_state.user = None

# Login and Registration
if st.session_state.user is None:

    option = st.sidebar.selectbox(
        "Select Option",
        ["Login", "Register"]
    )

    if option == "Register":

        st.subheader("User Registration")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Client", "Support"])

        if st.button("Register"):

            if username and password:
                result = register_user(username, password, role)

                if result:
                    st.success("Registration successful!")
                else:
                    st.error("Username already exists.")

            else:
                st.warning("Please fill all fields.")

    else:

        st.subheader("User Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            user = login_user(username, password)

            if user:
                st.session_state.user = user
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

# Logged-in user
else:

    username, role = st.session_state.user

    st.success(f"Welcome {username}!")
    st.write(f"Your role: {role}")

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()
