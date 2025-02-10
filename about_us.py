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
        .zoom-hover {{
            transition: transform 0.3s ease;
            display: inline-block;
        }}

        .zoom-hover:hover {{
            transform: scale(1.1);
        }}

        .separator {{
            margin: 0 10px;  /* Adjust space around the separator */
        }}
        </style>
        '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
    # Add a section for team members and affiliations
    # st.header("About Us")
    st.subheader("Team Members:")
    
    # Example of adding team members, their affiliations, and external links
    team_members = [
        {"name": "Mariano Forti", "affiliation": "Ruhr-Universität Bochum, Bochum, Nordrhein-Westfalen, Germany", "link": "https://www.mpie.de/4917874/Forti"},
        {"name": "Angelika Gedsun", "affiliation": "Albert-Ludwigs-Universität Freiburg, Freiburg im Breisgau, Baden-Württemberg, Germany", "link": "https://livmats.uni-freiburg.de/de/people/postdoctoral-researchers/angelika-gedsun"},
        {"name": "Yusra Shakeel", "affiliation": "KarlsruheInstitute of Technology, Kalrsruhe, Baden-Württemberg, Germany", "link": "https://www.dbse.ovgu.de/en/Staff/Externe+Doktoranden/Yusra+Shakeel.html"},
        {"name": "Ebrahim Norouzi", "affiliation": "FIZ Karlsruhe – Leibniz-Institute for Information Infrastructure GmbH, Kalrsruhe, Baden-Württemberg, Germany", "link": "https://www.fiz-karlsruhe.de/de/bereiche/lebenslauf-und-publikationen-ebrahim-norouzi"},
        {"name": "Ying Han", "affiliation": "Bundesanstalt für Materialforschungund-prüfung(BAM), Berlin, Germany", "link": "https://www.xing.com/profile/Ying_Han6"},
        {"name": "Luis Alexander Ávila Calderón ", "affiliation": "Bundesanstalt für Materialforschungund-prüfung(BAM), Berlin, Germany", "link": "https://www.researchgate.net/profile/Luis-Alexander-Avila/publications"},
         {"name": "Amirreza Daei Rezaei Moghaddam", "affiliation": "RWTH Aachen, Aachen, Nordrhein-Westfalen, Germany ", "link": "https://www.itc.rwth-aachen.de/cms/it-center/it-center/profil/team/~epvp/mitarbeiter-campus-/?gguid=PER-964N3TN&allou=1&lidx=1"},
        {"name": "Pavlina Kruzikova", "affiliation": "Bundesanstalt für Materialforschungund-prüfung(BAM), Berlin, Germany", "link": "https://www.linkedin.com/in/pavlina-kruzikova/?originalSubdomain=de"},
        {"name": "Amirhossein Bayani", "affiliation": "Albert-Ludwigs-Universität Freiburg, Freiburg im Breisgau, Baden-Württemberg, Germany", "link": "https://www.linkedin.com/in/amirhosseinbayani/"}
    ]
    
    for member in team_members:
        st.markdown(f'<a class="zoom-hover" href="{member["link"]}" target="_blank"><b>{member["name"]}</b></a><span class="separator"> - </span>{member["affiliation"]}', unsafe_allow_html=True)