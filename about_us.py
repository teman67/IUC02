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

def about_us_page():
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
    
    # Add a section for team members and affiliations
    # st.header("About Us")
    st.subheader("Team Members:")
    
    # Example of adding team members, their affiliations, and external links
    team_members = [
        {"name": "Angelika Gedsun", "affiliation": "IMTEK, Albert-Ludwigs-Universität Freiburg ", "link": "https://livmats.uni-freiburg.de/de/people/postdoctoral-researchers/angelika-gedsun"},
        {"name": "Yusra Shakeel", "affiliation": "Fakultät für Informatik, University Magdeburg", "link": "https://www.dbse.ovgu.de/en/Staff/Externe+Doktoranden/Yusra+Shakeel.html"},
        {"name": "Mariano Forti", "affiliation": "ICAMS, Ruhr university Bochum", "link": "https://www.mpie.de/4917874/Forti"},
        {"name": "Ying Han", "affiliation": "none", "link": "none"},
        {"name": "Luis Alexander Ávila", "affiliation": "Federal Institute for Materials Research and Testing (BAM), Berlin", "link": "https://www.researchgate.net/profile/Luis-Alexander-Avila/publications"},
        {"name": "Pavlina Kruzikova", "affiliation": "none", "link": "none"},
        {"name": "Amirhossein Bayani", "affiliation": "Livmats, Albert-Ludwigs-Universität Freiburg", "link": "https://www.linkedin.com/in/amirhosseinbayani/"}
    ]
    
    for member in team_members:
        st.markdown(f"[**{member['name']}**]( {member['link']} ) - {member['affiliation']}")
