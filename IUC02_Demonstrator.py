import streamlit as st
# from multipage_back import MultiPage

# Set page configuration here
st.set_page_config(page_title="IUC02", page_icon="🌐", layout="wide")

# Force light mode by defining primary colors manually
st.markdown(
    """
    <style>
    :root {
        --primary-color: #1f77b4;
        --background-color: #ffffff;
        --secondary-background-color: #f0f2f6;
        --text-color: #000000;
        --font: "sans-serif";
    }
    </style>
    """,
    unsafe_allow_html=True
)

from page_summary import page_summary
page_summary()