import streamlit as st
import math
import streamlit.components.v1 as components

def page_summary_body():

    # Set the page background image to appear on the right side
    page_bg_img = '''
    <style>
    [data-testid="stApp"] {
        background-color: white;  /* Set white background color */
        background-image: url("https://owncloud.fraunhofer.de/index.php/s/O8IEa05wALHXyVh/download?path=%2FLogos%20und%20Grafiken%2FLogo_NFDI-MatWerk%2F2020-07-03_neuesLogo&files=Logo_NFDI-MatWerk-1000px.png");
        background-position: 95% 95%;
        background-size: 40vh;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.markdown('<h3 style="color: black;">IUC02 Integration</h3>', unsafe_allow_html=True)

    container_size = 530  # px (canvas size)
    circle_size = 190  # px (individual circle size)
    big_circle_radius = 160  # Distance from center

    # Define links for circles
    links = [
        ("Metadata Ontology", "https://git.rwth-aachen.de/nfdi-matwerk/iuc02"),
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
                    border-radius: 50%; background-color: #3498db; color: black;
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
    components.html(f"<div style='text-align: center;'>{circle_html}</div>", height=container_size + 100)



    # footer_html = '''
    # <style>
    # .sidebar {
    #     display: flex;
    #     flex-direction: column;
    #     justify-content: space-between;
    #     height: 100vh;
    # }

    # .sidebar-content {
    #     flex-grow: 1;
    # }

    # .sidebar-footer {
    #     background-color: #333;
    #     color: white;
    #     text-align: center;
    #     padding: 10px;
    #     margin-top: 70vh;
    #     font-size: 14px;
    # }

    # .sidebar-footer a {
    #     color: white;
    #     text-decoration: none;
    #     margin: 0 10px;
    #     font-size: 20px;
    # }

    # .sidebar-footer a:hover {
    #     color: #2ecc71;  /* Change color on hover */
    # }
    # </style>

    # <div class="sidebar-content">
    #     <!-- Sidebar content here -->
    # </div>

    # <div class="sidebar-footer">
    #     Developed by A. Bayani
    #     <a href="https://github.com/teman67" target="_blank">
    #         <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/1024px-Octicons-mark-github.svg.png" alt="GitHub" style="width: 25px; height: 25px; vertical-align: middle;">
    #     </a>
    #     <a href="https://www.linkedin.com/in/amirhosseinbayani/" target="_blank">
    #         <img src="https://upload.wikimedia.org/wikipedia/commons/7/7d/LinkedIn_Logo_2023.png" alt="LinkedIn" style="width: 20px; height: 20px; vertical-align: middle;">
    #     </a>
    # </div>
    # '''

    # # Display the footer in the sidebar
    # st.sidebar.markdown(footer_html, unsafe_allow_html=True)
