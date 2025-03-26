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
image_path = os.path.join(current_dir, "../images/Nfdi_Matwer_logo.png")

if os.path.exists(image_path):
    base64_img = get_base64_encoded_image(image_path)
else:
    st.error(f"Image not found: {image_path}")

def get_example_file(file_path):
    """Reads and returns the content of an example file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def data_validation_page():
    st.set_page_config(layout="wide")
    st.markdown('''
    ## Data Validation Workflow 

    - In this Data Validation Workflow you can explore how the exemplary *Data Graph* (*populated with data from the Reference data on creep*) is validated against predefined SHACL Shapes (requirements the data has to fulfil, e.g. mandatory fields are present, and follows a specific datatype).
    
    - For this step the SHACL Shapes needs to be predefined. (**Shape Graph**). 

    - The output of the Validation Process is the Validation protocol, which reports the violations of the **SHACL constrains**.

    - You can use your own *Data Graph* and *SHACL Shapes* in this **Data Validation Workflow**. 
                
    - The Script for the validation is running in the backend and can be accessed in the [Git Repository](https://git.rwth-aachen.de/nfdi-matwerk/iuc02/-/blob/main/Demonstrator_App/pages/Data_Validation.py). 
    ''', unsafe_allow_html=True)

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
        .section-box {{
            border: 1px solid #05445e;
            padding: 1px;
            margin: 10px 0;
            border-radius: 10px;
            background-color: #05445e;
        }}
        </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
            div[data-testid="stFileUploader"] {
                width: 600px !important;
                padding: 5px !important;
            }
            .stDownloadButton {
                margin-top: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # st.markdown('''
    # <h2 style=" text-align: left; margin-bottom: 5px">
    #     SHACL Validator
    # </h2>
    # <h3 style=" text-align: left; margin-top: 0px; margin-bottom: 2px">
    #     This page allows you to validate your data against a SHACL shape.
    # </h3>
    # <h4 style=" text-align: left; margin-top: 0px; margin-bottom: 20px">
    #     Please upload your data and SHACL shape files below or use the example files.
    # </h4>
    # ''', unsafe_allow_html=True)

    # Example file paths
    example_rdf_path = "./data/rdfGraph_smallExample.ttl"  
    example_shacl_path = "./data/shaclShape_smallExample.ttl"  

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    with col1:
        rdf_file_option = st.radio(
            "Select Data Graph file:",
            options=["Upload Your Own", "Use Example Data Graph"],
            index=0
        )

        rdf_content = None
        if rdf_file_option == "Upload Your Own":
            rdf_file = st.file_uploader("Upload Data Graph (Turtle format)", type=["ttl"])
            if rdf_file:
                rdf_content = rdf_file.read().decode("utf-8")  # Read content
        else:
            rdf_content = get_example_file(example_rdf_path)

        # Text area to edit RDF file content
        if rdf_content:
            rdf_content = st.text_area("Edit Data Graph", rdf_content, height=300)
            if st.button("Submit Edited Data Graph"):
                st.success("Data Graph submitted successfully!")

    with col2:
        with open(example_rdf_path, "r") as f:
            rdf_example = f.read()
        st.download_button("Download Example Data Graph", rdf_example, "example_data.ttl", "application/x-turtle")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    col3, col4 = st.columns([1, 1])

    with col3:
        shacl_file_option = st.radio(
            "Select Shape Graph file:",
            options=["Upload Your Own", "Use Example Shape Graph"],
            index=0
        )

        shacl_content = None
        if shacl_file_option == "Upload Your Own":
            shacl_file = st.file_uploader("Upload Shape Graph (Turtle format)", type=["ttl"])
            if shacl_file:
                shacl_content = shacl_file.read().decode("utf-8")  # Read content
        else:
            shacl_content = get_example_file(example_shacl_path)

        # Text area to edit SHACL file content
        if shacl_content:
            shacl_content = st.text_area("Edit Shape Graph", shacl_content, height=300)
            if st.button("Submit Edited Shape Graph"):
                st.success("Shape Graph submitted successfully!")

    with col4:
        with open(example_shacl_path, "r") as f:
            shacl_example = f.read()
        st.download_button("Download Example Shape Graph", shacl_example, "example_shacl.ttl", "application/x-turtle")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    # Button to validate the files
    if st.button("Validate Data Against SHACL"):
        if rdf_content and shacl_content:
            try:
                # Load RDF file content
                g = Graph()
                g.parse(data=rdf_content, format="turtle")
                st.success("RDF file is valid!")

                json_ld_data = g.serialize(format="json-ld", indent=4)
                st.download_button("Download JSON-LD", json_ld_data, "dataGraph.jsonld", "application/json")

                # Load SHACL file content
                shacl_shape = Graph()
                shacl_shape.parse(data=shacl_content, format="turtle")

                # Validate RDF against SHACL
                results = validate(
                    g,
                    shacl_graph=shacl_shape,
                    inference='rdfs',
                    data_graph_format="turtle",
                    shacl_graph_format="turtle",
                    abort_on_first=False,
                    allow_infos=False,
                    allow_warnings=False,
                    meta_shacl=False,
                    advanced=False,
                    js=False,
                    debug=True,
                    serialize_report_graph="ttl"
                )
                conforms, report_graph, report_text = results

                st.write("**Validation Result:**")
                st.warning(f"Conforms: {conforms}")
                st.text_area("SHACL Report", report_text, height=300)

                report_g = Graph()
                report_g.parse(data=report_graph, format="turtle", encoding="utf-8")

                st.write("## Detailed SHACL Report")
                st.write("Below is a structured view of the SHACL validation report:")

                for s, p, o in sorted(report_g):
                    st.markdown(f"- **Subject:** `{s}`\n  - **Predicate:** `{p}`\n  - **Object:** `{o}`")

            except Exception as e:
                st.error(f"Error processing files: {e}")
        else:
            st.warning("Please upload or select example files before validation.")


data_validation_page()