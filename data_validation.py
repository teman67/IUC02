import streamlit as st
import pyshacl
from pyshacl import validate
from rdflib import Graph


def get_example_file(file_path):
    """Reads and returns the content of an example file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def data_validation_page():
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
    <h1 style=" text-align: left; margin-bottom: 10px">
        RDF SHACL Validator
    </h1>
    <h3 style=" text-align: left; margin-top: 0px; margin-bottom: 2px">
        This page allows you to validate your data against a SHACL shape.
    </h3>
    <h4 style=" text-align: left; margin-top: 0px; margin-bottom: 30px">
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
            "Select RDF file:",
            options=["Upload Your Own", "Use Example RDF"],
            index=0
        )

        if rdf_file_option == "Upload Your Own":
            rdf_file = st.file_uploader("Upload RDF (Turtle format)", type=["ttl"])
        else:
            # Use example RDF file
            rdf_content = get_example_file(example_rdf_path)
            rdf_file = rdf_content

    with col2:
        with open(example_rdf_path, "r") as f:
            rdf_example = f.read()
        st.download_button("Download Example RDF", rdf_example, "example_data.ttl", "application/x-turtle")

    # SHACL Upload and Download
    col3, col4 = st.columns([1, 1])

    with col3:
        shacl_file_option = st.radio(
            "Select SHACL file:",
            options=["Upload Your Own", "Use Example SHACL"],
            index=0
        )

        if shacl_file_option == "Upload Your Own":
            shacl_file = st.file_uploader("Upload SHACL (Turtle format)", type=["ttl"])
        else:
            # Use example SHACL file
            shacl_content = get_example_file(example_shacl_path)
            shacl_file = shacl_content

    with col4:
        with open(example_shacl_path, "r") as f:
            shacl_example = f.read()
        st.download_button("Download Example SHACL", shacl_example, "example_shacl.ttl", "application/x-turtle")

    # Process files
    if rdf_file and shacl_file:
        try:
            # Load RDF file content (either uploaded or example)
            g = Graph()
            if isinstance(rdf_file, bytes):
                g.parse(data=rdf_file, format="turtle")
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


# Run the function
data_validation_page()
