import streamlit as st
import math
import streamlit.components.v1 as components

def page_summary_body():

    st.markdown("<h1 style='text-align: center;'>IUC02</h1>", unsafe_allow_html=True)

    container_size = 620  # px (canvas size)
    circle_size = 220  # px (individual circle size)
    big_circle_radius = 190  # Distance from center

    # Define links for circles
    links = [
        ("Metadata Ontology", "https://www.google.com"),
        ("MSE Knowledge Graph", "http://en.lodlive.it/?https://purls.helmholtz-metadaten.de/msekg/E1173747"),
        ("Fair Digital Object", "https://kit-data-manager.github.io/fairdoscope/"),
        ("Data Retrieval", "https://git.rwth-aachen.de/nfdi-matwerk/iuc02"),
        ("Dataset Validation", "https://ulb-darmstadt.github.io/shacl-form/#example"),
    ]

    # Generate circle positions using trigonometry
    circle_html = f'''
        <div style="position: relative; width: {container_size}px; height: {container_size}px; margin: auto;">
    '''
    for i, (text, url) in enumerate(links):
        angle = (2 * math.pi / len(links)) * i  # Evenly distribute circles
        x = container_size / 2 + big_circle_radius * math.cos(angle) - circle_size / 2
        y = container_size / 2 + big_circle_radius * math.sin(angle) - circle_size / 2
        circle_html += f'''
            <a href="{url}" target="_blank" 
            style="position: absolute; left: {x}px; top: {y}px;
                    width: {circle_size}px; height: {circle_size}px;
                    border-radius: 50%; background-color: #3498db; color: white;
                    font-size: 20px; font-weight: bold;
                    text-decoration: none; display: flex;
                    align-items: center; justify-content: center;
                    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
                    transition: transform 0.2s ease-in-out, background-color 0.3s ease-in-out;">
            {text}
            </a>
        '''

    circle_html += """
    <style>
        a:hover {
            background-color: #2ecc71 !important;  /* Change to green on hover */
            transform: scale(1.2);  /* Zoom in */
        }
    </style>
    """

    # Use components.html to correctly render the HTML and CSS
    components.html(f"<div style='text-align: center;'>{circle_html}</div>", height=container_size + 50)
