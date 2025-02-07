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


def data_validation_page():
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

    st.markdown('''
    <h2 style=" text-align: left; margin-bottom: 5px">
        SHACL Validator
    </h2>
    <h3 style=" text-align: left; margin-top: 0px; margin-bottom: 2px">
        This page allows you to validate your data against a SHACL shape.
    </h3>
    <h4 style=" text-align: left; margin-top: 0px; margin-bottom: 20px">
        Please upload your data and SHACL shape files below or use the example files.
    </h4>
    ''', unsafe_allow_html=True)

    # Example file paths
    example_rdf_path = "rdfGraph_smallExample.ttl"  # Path to your example RDF file
    example_shacl_path = "shaclShape_smallExample.ttl"  # Path to your example SHACL file

    # Create columns for file upload and download buttons
    col1, col2 = st.columns([1, 1])

    # RDF Upload and Download
    with col1:
        rdf_file_option = st.radio(
            "Select Data Graph file:",
            options=["Upload Your Own", "Use Example Data Graph"],
            index=0
        )

        if rdf_file_option == "Upload Your Own":
            rdf_file = st.file_uploader("Upload Data Graph (Turtle format)", type=["ttl"])
        else:
            # Use example RDF file
            rdf_content = get_example_file(example_rdf_path)
            rdf_file = rdf_content

    with col2:
        with open(example_rdf_path, "r") as f:
            rdf_example = f.read()
        st.download_button("Download Example Data Graph", rdf_example, "example_data.ttl", "application/x-turtle")

    # SHACL Upload and Download
    col3, col4 = st.columns([1, 1])

    with col3:
        shacl_file_option = st.radio(
            "Select Shape Graph file:",
            options=["Upload Your Own", "Use Example Shape Graph"],
            index=0
        )

        if shacl_file_option == "Upload Your Own":
            shacl_file = st.file_uploader("Upload Shape Graph (Turtle format)", type=["ttl"])
        else:
            # Use example SHACL file
            shacl_content = get_example_file(example_shacl_path)
            shacl_file = shacl_content

    with col4:
        with open(example_shacl_path, "r") as f:
            shacl_example = f.read()
        st.download_button("Download Example Shape Graph", shacl_example, "example_shacl.ttl", "application/x-turtle")

    # Process files
    if rdf_file and shacl_file:
        try:
            # Load RDF file content (either uploaded or example)
            g = Graph()

            # Check if file is an instance of UploadedFile and read the content as bytes
            if isinstance(rdf_file, bytes):
                g.parse(data=rdf_file, format="turtle")
            elif isinstance(rdf_file, st.runtime.uploaded_file_manager.UploadedFile):
                rdf_bytes = rdf_file.read()  # Read file content as bytes
                g.parse(data=rdf_bytes, format="turtle")
            else:
                g.parse(data=rdf_file, format="turtle")
                
            st.success("RDF file is valid!")

            # Convert RDF to JSON-LD
            json_ld_data = g.serialize(format="json-ld", indent=4)
            st.download_button("Download JSON-LD", json_ld_data, "dataGraph.jsonld", "application/json")

            # Load SHACL file content (either uploaded or example)
            shacl_shape = Graph()
            if isinstance(shacl_file, bytes):
                shacl_shape.parse(data=shacl_file, format="turtle")
            elif isinstance(shacl_file, st.runtime.uploaded_file_manager.UploadedFile):
                shacl_bytes = shacl_file.read()  # Read file content as bytes
                shacl_shape.parse(data=shacl_bytes, format="turtle")
            else:
                shacl_shape.parse(data=shacl_file, format="turtle")

            # Validate RDF against SHACL
            results = validate(
                g,
                shacl_graph=shacl_shape,
                inference='rdfs',
                data_graph_format="json-ld",
                shacl_graph_format="ttl",
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
            report_g.parse(data=report_graph, format="ttl", encoding="utf-8")

            st.write("## Detailed SHACL Report")
            st.write("Below is a structured view of the SHACL validation report:")

            for s, p, o in sorted(report_g):
                st.markdown(f"- **Subject:** `{s}`\n  - **Predicate:** `{p}`\n  - **Object:** `{o}`")

        except Exception as e:
            st.error(f"Error processing files: {e}")


