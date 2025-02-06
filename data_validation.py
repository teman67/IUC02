import streamlit as st
import pyshacl
from pyshacl import validate
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD
import sys



def data_validation_page():
    st.title("RDF SHACL Validator")
    st.write("This page allows you to validate your data against a SHACL shape.")
    st.write("Please upload your data and SHACL shape files below.")

    
    rdf_file = st.file_uploader("Upload RDF (Turtle format)", type=["ttl"])
    shacl_file = st.file_uploader("Upload SHACL (Turtle format)", type=["ttl"])

    if rdf_file and shacl_file:
        try:
            # Load RDF file
            g = Graph()
            g.parse(rdf_file, format="turtle")
            st.success("RDF file is valid!")
            
            # Convert RDF to JSON-LD
            json_ld_data = g.serialize(format="json-ld", indent=4)
            st.download_button("Download JSON-LD", json_ld_data, "dataGraph.jsonld", "application/json")
            
            # Load SHACL file
            shacl_shape = Graph()
            shacl_shape.parse(shacl_file, format="turtle")
            
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
            st.write(f"Conforms: {conforms}")
            st.text_area("SHACL Report", report_text, height=300)
            
            report_g = Graph()
            report_g.parse(data=report_graph, format="ttl", encoding="utf-8")
            
            st.write("## Detailed SHACL Report")
            st.write("Below is a structured view of the SHACL validation report:")
            
            for s, p, o in sorted(report_g):
                st.markdown(f"- **Subject:** `{s}`\n  - **Predicate:** `{p}`\n  - **Object:** `{o}`")
        
        except Exception as e:
            st.error(f"Error processing files: {e}")

