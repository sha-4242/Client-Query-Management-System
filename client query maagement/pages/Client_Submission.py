
import streamlit as st
from database.db import insert_query

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef2ff, #f5f3ff);
}

h1 {
    color: #4338ca !important;
    font-weight: 800;
}

h2, h3 {
    color: #4f46e5 !important;
}

.stButton > button {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
    font-weight: bold;
}

.stButton > button:hover {
    background: #3730a3;
    color: white;
    border: none;
}

input, textarea {
    border-radius: 8px !important;
}

</style>
""", unsafe_allow_html=True)


st.set_page_config(
    page_title="Client Query Submission",
    page_icon="📩",
    layout="centered"
)

st.title("📩 Client Query Submission")
st.write("Submit your query to our support team.")

email = st.text_input("Email Address")
mobile = st.text_input("Mobile Number")
heading = st.text_input("Query Heading")

category = st.selectbox(
    "Query Category",
    [
        "Technical Issue",
        "Billing",
        "Account Issue",
        "General Inquiry"
    ]
)

description = st.text_area("Query Description")

if st.button("Submit Query"):

    if email and mobile and heading and description:

        try:
            insert_query(
                email,
                mobile,
                heading,
                description,
                category
            )

            st.success("Query submitted successfully!")

        except Exception as e:
            st.error(f"Error submitting query: {e}")

    else:
        st.warning("Please fill in all fields.")
