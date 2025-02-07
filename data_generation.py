import streamlit as st
import pyshacl
from pyshacl import validate
from rdflib import Graph
import base64
import os

def get_base64_encoded_image(image_path):
    """Convert image to Base64."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Use absolute path
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "Nfdi_Matwer_logo.png")

if os.path.exists(image_path):
    base64_img = get_base64_encoded_image(image_path)
else:
    st.error(f"Image not found: {image_path}")

def get_example_file(file_path):
    """Reads and returns the content of an example file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


import streamlit as st

def data_generation_page():
    # Set the page background image
    page_bg_img = f'''
        <style>
        [data-testid="stApp"] {{
            background-color: white;
            background-image: url("data:image/png;base64,{base64_img}");
            background-position: 95% 95%;
            background-size: 20vh;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.markdown('''
    <h3 style="color: black; text-align: left; margin-bottom: 50px">
        From Data Generation to Data Validation
    </h3>
    '''
    , unsafe_allow_html=True)

    # File URLs (Replace these with actual URLs or paths)
    file1 = "Vh5205_C-95.LIS"  # File for Step 1
    file2 = "Vh5205_C-95_translated.json"  # File for Step 2
    file3a = "rdfGraph_smallExample.ttl"  # First file for Step 3
    file3b = "shaclShape_smallExample.ttl"  # Second file for Step 3
    ext_file1 = "mapping document.json"  # First file for Extra Step
    ext_file2 = "2024-09_Schema_IUC02_v1.json"  # Second file for Extra Step

    # First row for extra box above the first arrow
    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 2, 1, 2, 1, 2])

    with col2:
        st.markdown(
            f'''
            <div style="padding:10px; border:2px solid black; text-align:center; background-color:#FFCDD2; border-radius:10px;">
                <b>Mapping Step</b><br>
                <a href="{ext_file2}" download style="color:blue; text-decoration:none;">Metadata Schema</a><br>
                <a href="{ext_file1}" download style="color:blue; text-decoration:none;">Mapping Document</a>
            </div>
            ''',
            unsafe_allow_html=True
        )

    # Add space to separate extra box from main flow
    st.markdown("<br>", unsafe_allow_html=True)

    # Second row for the main workflow (aligned in a straight line)
    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 2, 1, 2, 1, 2])

    with col1:
        st.markdown(
            f'''
            <div style="padding:20px; border:2px solid black; text-align:center; background-color:#E3F2FD; border-radius:10px;">
                <b>Creep experiment input file (.lis file)</b><br>
                <a href="{file1}" download style="color:blue; text-decoration:none;">Download</a>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown('<div style="text-align:center; font-size:30px;">↓</div>', unsafe_allow_html=True)  # Down arrow
        st.markdown('<div style="text-align:center; font-size:40px;">→</div>', unsafe_allow_html=True)  # Right arrow

    with col3:
        st.markdown(
            f'''
            <div style="padding:20px; border:2px solid black; text-align:center; background-color:#BBDEFB; border-radius:10px;">
                <b>Populated Schema</b><br>
                <a href="{file2}" download style="color:blue; text-decoration:none;">Download</a>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with col4:
        st.markdown('<div style="text-align:center; font-size:40px;">→</div>', unsafe_allow_html=True)

    with col5:
        st.markdown(
            f'''
            <div style="padding:20px; border:2px solid black; text-align:center; background-color:#90CAF9; border-radius:10px;">
                <b>Step 3</b><br>
                <a href="{file3a}" download style="color:blue; text-decoration:none;">Data Graph</a><br>
                <a href="{file3b}" download style="color:blue; text-decoration:none;">Shape Graph</a>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with col6:
        st.markdown('<div style="text-align:center; font-size:40px;">→</div>', unsafe_allow_html=True)

    with col7:
        st.markdown(
            f'''
            <div style="padding:20px; border:2px solid black; text-align:center; background-color:#64B5F6; border-radius:10px;">
                <b>Validation Protocol</b>
            </div>
            ''',
            unsafe_allow_html=True
        )

