import streamlit as st
import streamlit.components.v1 as components
import base64
import os


import time

# Function to check if the warning message has been shown
def check_warning_message_state():
    '''
    Checks if the warning message has been shown.
    '''

    if 'warning_shown' not in st.session_state:
        st.session_state.warning_shown = False

# Function to show the warning message
def show_warning_message():
    '''
    Displays the warning message recommending light mode over dark mode.
    '''

    if not st.session_state.warning_shown:
        placeholder = st.empty()
        placeholder.markdown('<div style="background-color: #FFEEEB; padding: 30px; margin-top: 40px; border-radius: 5px; text-align: center;"><p style="font-size: 20px; color: #333333"><strong>For better visualization, it is recommended to use Light mode instead of Dark mode in Settings (top right).</strong></p></div>', unsafe_allow_html=True)
        st.session_state.warning_shown = True

        time.sleep(5)  # Wait for 5 seconds
        placeholder.empty()


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


def page_summary_body():
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

    '''
    Displays the page summary body including project details and a warning message.
    '''

    check_warning_message_state()
    show_warning_message()


    st.markdown('''
    <h3 style="color: black; text-align: left; margin-bottom: 0px">
        IUC02: Framework for Curation and Distribution of Reference Datasets
    </h3>
    <h3 style="color: black; text-align: left; margin-top: 0px; margin-bottom: 20px">
        (on the Example of Creep Data of Ni-Based Superalloys)
    </h3>
    '''
    , unsafe_allow_html=True)
    
    # Add descriptive text above the workflow
    description_text = '''
    <p style="text-align: justify; font-size: 18px; color: black; margin: auto;">
    The aim of this IUC is to develop a framework for reference material data sets using creep properties of single crystal Ni-based superalloy as example. 
    Such reference data sets are necessary for (i) evaluating and validating experimental/modeling methods and their uncertainties, 
    (ii) assessing the performance of analysis, modelling and simulation tools by use of standardized processes and 
    (iii) providing comprehensive material descriptions (e.g., meta-data schemas and ontologies). 
    Community-driven processes will be established for the definition, identification and curation of reference material data sets, including metadata, raw data and processed data, and quality assessment routines. 
    Reference data set will contain detailed meta-data and context concerning materials history, data collection (e.g., testing and measurement equipment, calibration status/certificate) 
    and the related specific uncertainty/error (measurement, model, simulation). Existing data on Ni-base superalloys from PP18 BAM and PP01 SFB/TR103 will be used, 
    where superalloys have been well characterized using a broad spectrum of characterization methods and in-depth data is available.
    </p>
    '''
    st.markdown(description_text, unsafe_allow_html=True)

    # Define workflow steps
    # Define workflow steps
    steps = [
        ("Data Generation", "https://git.rwth-aachen.de/nfdi-matwerk/iuc02", []),
        ("Semantic Resources and Metadata Schema", "https://git.rwth-aachen.de/nfdi-matwerk/iuc02", [
            "Json Metadata Schema",
            "Reference Data Set (for creep data)",
            "RDO(C)",
            "SCHACL Shape",
        ]),
        ("Data Validation", "https://ulb-darmstadt.github.io/shacl-form/#example", []),
        ("MSE Knowledge Graph", "http://en.lodlive.it/?https://purls.helmholtz-metadaten.de/msekg/E1173747", []),
        ("Fair Digital Objects (FDO)", "https://kit-data-manager.github.io/fairdoscope/", []),
    ]

    # Generate workflow as horizontal boxes
    workflow_html = """
    <div style="display: flex; justify-content: center; align-items: center; gap: 20px; margin-top: 50px;">
    """

    for text, url, bullet_points in steps:
        if bullet_points:
            # Special larger box for "Semantic Resources and Metadata Schema"
            workflow_html += f'''
                <div class="hover-box large-box" onclick="window.open('{url}', '_blank')">
                    <a href="{url}" target="_blank">{text}</a>
                    <ul>
            '''
            for bullet in bullet_points:
                workflow_html += f'<li>{bullet}</li>'
            workflow_html += '</ul></div>'
        
        else:
            # Standard box for other steps
            workflow_html += f'''
                <a href="{url}" target="_blank" class="hover-box">
                    {text}
                </a>
            '''

    workflow_html += """
    </div>
    <style>
        /* Default Box Style */
        .hover-box {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 210px;
            height: 70px;
            padding: 10px;
            background-color: #3498db;
            color: white;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s ease-in-out, background-color 0.3s ease-in-out;
            cursor: pointer;
            text-decoration: none; /* Remove underline */
        }

        /* Larger Box for "Semantic Resources and Metadata Schema" */
        .large-box {
            width: 280px; /* Increased width */
            height: 140px; /* Increased height */
        }

        .hover-box a {
            color: white;
            text-decoration: none; /* Remove underline from links */
        }

        .hover-box ul {
            list-style-type: disc;
            padding-left: 15px;
            text-align: left;
            font-size: 14px;
            margin-top: 10px;
        }

        .hover-box:hover {
            background-color: #05445e;
            transform: scale(1.05);
        }
    </style>
    """

    # Render the HTML component
    components.html(workflow_html, height=250)
