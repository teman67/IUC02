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
    with open(file_path, "r", encoding="latin-1") as f:
        return f.read()
    
def read_file(file_path):
    """Safely read the file with multiple encoding attempts."""
    encodings_to_try = [ 'ISO-8859-1']
    
    for encoding in encodings_to_try:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue  # Try the next encoding
    
    # If all attempts fail, raise an error
    raise UnicodeDecodeError(f"Failed to decode {file_path} with all attempted encodings.")

def data_generation_page():
    st.set_page_config(layout="wide")
    st.markdown('''
    ## Data Generation Workflow

    The **Data Generation Workflow** represents how you can prepare the resources needed to validate your Data Graph.

    **Step 1:** Download your data from the repository. The demonstrator shows the *Creep Experiment Input File*, downloaded from [Zenodo](https://zenodo.org/records/13937987).

    **Step 2:** Populate the JSON Metadata Schema with data from your Input file. This step requires:
    - A **JSON Metadata Schema** 
    - A **Mapping Document** to correctly parse the Input data.

    The Metadata Schema can be accessed in the [Git Repository](https://git.rwth-aachen.de/nfdi-matwerk/iuc02/-/tree/main/Data%20Schema).

    **Step 3:** Generate the **Populated Data Graph (RDF-Graph)** from the Populated Metadata Schema using Ontology entities. 
    - This step requires an **Ontology**, which can be accessed in the same [Git Repository](https://git.rwth-aachen.de/nfdi-matwerk/iuc02/-/tree/main/Ontology%20Development).

    **Step 4:** Validate the Data Graph against predefined **SHACL Shapes** to ensure:
    - Mandatory fields are present.
    - The data follows a specific datatype.

    The SHACL Shapes can be accessed in the [Git Repository](https://git.rwth-aachen.de/nfdi-matwerk/iuc02).

    The **output of the Validation Process** is the **Validation Protocol**.

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
        </style>
        '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # st.markdown('''
    # <h3 style="color: black; text-align: left; margin-bottom: 50px">
    #     From Data Generation to Data Validation
    # </h3>
    # ''', unsafe_allow_html=True)

    # File URLs (Replace these with actual URLs or paths)
    file1 = "./data/Vh5205_C-95.LIS"  # File for Step 1
    file2 = "./data/Vh5205_C-95_translated.json"  # File for Step 2
    file3a = "./data/rdfGraph_smallExample.ttl"  # First file for Step 3
    file3b = "./data/shaclShape_smallExample.ttl"  # Second file for Step 3
    ext_file1 = "./data/mapping document.json"  # First file for Extra Step
    ext_file2 = "./data/2024-09_Schema_IUC02_v1.json"  # Second file for Extra Step

    # First row for extra box above the first arrow
    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 2, 1, 2, 1, 2])

    with col2:
        st.markdown(
            f'''
            <div style="padding:20px; border:2px solid black; text-align:center; 
                        background-color:#05445e; border-radius:10px; color:white; 
                        font-size:18px; min-width:250px; 
                        margin-left: -85px; margin-bottom: -100px">  
                <b>Mapping <img src="https://about.gitlab.com/images/press/logo/png/gitlab-icon-rgb.png" 
                    alt="GitLab" width="60" height="60" style="margin-left: 170px; margin-top:-40px; margin-right:10px;"></b><br>
                <li>Metadata Schema</li>
                <li>Mapping Document</li>
            </div>
            ''',
            unsafe_allow_html=True
        )



    # Add space to separate extra box from main flow
    st.markdown("<br>", unsafe_allow_html=True)

    # First row for extra box above the first arrow
    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 2, 1, 2, 1, 2])

    with col5:
        st.markdown(
            f'''
            <div style="padding:15px; border:2px solid black; text-align:center;
                        background-color:#05445e; border-radius:10px; color:white; 
                        min-width:50px;  margin-bottom: 0px; margin-top: -10px; max-width:180px; margin-left: -110px;
                        ">  
                <b><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTm8U7AGVOvLM-YbLe8fGD8cfqXmXQSY7umTQ&s" 
                    alt="RDF" width="40" height="40" style="margin-top: -70px; margin-left: -65px; margin-right:10px;">Ontology (Graph)</b><br>
            </div>
            ''',
            unsafe_allow_html=True
        )

    # Add space to separate extra box from main flow
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 2, 1, 2, 1, 2])

    with col7:
        st.markdown(
            f'''
            <div style="padding:15px; border:2px solid black; text-align:center;
                        background-color:#05445e; border-radius:10px; color:white; 
                          margin-bottom: 0px; margin-top: -84px; margin-left:-200px; max-width:180px; 
                        "> 
                <b><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQUjbiGuDUs4poajSf5Uw-ePPQFlvaPiyNX7Q&s " 
                    alt="SHACL" width="40" height="40" style="margin-top: -70px; margin-left: -65px; margin-right:10px;">SHACL Shapes </b><br>
            </div>
            ''',
            unsafe_allow_html=True
        )

    # Add space to separate extra box from main flow
    st.markdown("<br>", unsafe_allow_html=True)
    with col5:
        st.markdown('<div style="text-align:center; font-size:40px; margin-top: -10px; font-weight:bold; ">↓</div>', unsafe_allow_html=True)

    # with col6:
    #     st.markdown('<div style="text-align:center; font-size:40px; margin-top: -50px; font-weight:bold; ">↓</div>', unsafe_allow_html=True)


    # Second row for the main workflow (aligned in a straight line)
    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 2, 1, 2, 1, 2])

    with col1:
        # with open(file1, "rb") as f:
        #     file_bytes = f.read()
        with st.container():
            st.markdown(
                """
                <div style="padding:20px; border:2px solid black; text-align:center; background-color:#E3F2FD; border-radius:10px; margin-top: -30px">
                    <b><img src="https://static.thenounproject.com/png/2952643-200.png" 
                    alt="Input Data" width="40" height="40" style="margin-top: -60px; margin-left: -50px;"> Creep experiment input file (.lis file)</b><br>
                </div>
                """,
                unsafe_allow_html=True
            )

            # st.download_button(
            #     label="Download File",
            #     data=file_bytes,
            #     file_name="file1",
            #     mime="application/octet-stream"
            # )

    with col2:
        st.markdown('<div style="text-align:center; font-size:40px; font-weight:bold; margin-top: -80px;">↓</div>', unsafe_allow_html=True)  # Down arrow
        st.markdown('<div style="text-align:center; font-size:40px; margin-top: -50px; font-weight:bold; ">→</div>', unsafe_allow_html=True)  # Right arrow

    with col3:
        st.markdown(
            f'''
            <div style="padding:20px; border:2px solid black; text-align:center; background-color:#BBDEFB; border-radius:10px; margin-top: -30px;">
                <b><img src="https://res.cloudinary.com/dlthn5m1i/image/upload/v1742823071/JSON_schema_xlril2.png" 
                    alt="JSON Schema" width="80" height="30" style="margin-top: -70px; margin-left: -70px;">Populated metadata schema</b><br>
            </div>
            ''',
            unsafe_allow_html=True
            
        )

    with col4:
        st.markdown('<div style="text-align:center; font-size:40px; margin-top: -30px; font-weight:bold; ">→</div>', unsafe_allow_html=True)

    with col5:
        st.markdown(
            f'''
            <div style="padding:20px; border:2px solid black; text-align:center; background-color:#90CAF9; border-radius:10px; margin-top: -30px;">
                <b><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTm8U7AGVOvLM-YbLe8fGD8cfqXmXQSY7umTQ&s" 
                    alt="RDF" width="40" height="40" style="margin-top: -70px; margin-left: -45px; margin-right:10px;">Populated Data Graph</b><br>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with col6:
        st.markdown('<div style="text-align:center; font-size:40px; margin-top: -30px; font-weight:bold; ">→</div>', unsafe_allow_html=True)

    with col7:
        st.markdown(
            f'''
            <div style="padding:20px; border:2px solid black; text-align:center; background-color:#64B5F6; border-radius:10px; margin-top: -30px;">
                <b><img src="https://cdn-icons-png.freepik.com/512/5531/5531412.png" 
                    alt="Validation" width="60" height="60" style="margin-top: -70px; margin-left: -45px; margin-right:10px;">Validation Protocol</b>
            </div>
            ''',
            unsafe_allow_html=True
        )
    
    # # Display file content in editable mode
    # file_to_edit = st.selectbox("Choose a file to edit:", [file1, file2, file3a, file3b, ext_file1, ext_file2])
    # if file_to_edit:
    #     file_content = get_example_file(file_to_edit)
    #     edited_content = st.text_area("Edit File Content", value=file_content, height=300)
    #     if st.button("Save Changes"):
    #         # Save the edited content back to the file
    #         with open(file_to_edit, "w", encoding="latin-1") as f:
    #             f.write(edited_content)
    #         st.success(f"File '{file_to_edit}' has been updated.")

    # File selection & editing
    st.markdown(
    """
    <style>
    .custom-header {
        font-size: 30px;
        
        font-weight: bold;
        
        margin-top: 50px;
        padding: 0px;
        
        
    }
    </style>
    <div class="custom-header">Show and Edit Files</div>
    """,
    unsafe_allow_html=True
    )

    # Mapping file names to user-friendly labels
    file_options = {
        "./data/Vh5205_C-95.LIS": "Creep Experiment Input File",
        "./data/Vh5205_C-95_translated.json": "Populated Metadata Schema",
        "./data/rdfGraph_smallExample.ttl": "Populated Data Graph",
        "./data/shaclShape_smallExample.ttl": "Shape Graph",
        "./data/mapping document.json": "Mapping Document",
        "./data/2024-09_Schema_IUC02_v1.json": "Metadata Schema"
    }

    st.markdown(
        """
        <style>
        .streamlit-expanderHeader {
            font-size: 14px;
        }
        div[data-baseweb="select"] {
            width: 400px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Dropdown to select a file (show friendly names)
    selected_label = st.selectbox("Choose a file:", list(file_options.values()))

    # Reverse lookup: Find the actual filename
    file_to_edit = next((key for key, value in file_options.items() if value == selected_label), None)

    if "selected_file" not in st.session_state:
        st.session_state.selected_file = None

    if st.button("Load File"):
        st.session_state.selected_file = file_to_edit

    if st.session_state.selected_file == file_to_edit:
        file_content = read_file(file_to_edit)
        edited_content = st.text_area("Edit File Content", value=file_content, height=400)

        # Extract file extension from the original file
        file_extension = file_to_edit.split('.')[-1]
        
        # st.button("Download Edited File"):
        # Convert the edited content to bytes for download
        edited_file_bytes = edited_content.encode("latin-1")

        # Update the file name with the original extension
        file_name_with_extension = f"{selected_label.split('.')[0]}.{file_extension}"

        st.download_button(
            label="Download Edited File",
            data=edited_file_bytes,
            file_name=file_name_with_extension,
            mime="application/octet-stream"
        )

    st.markdown('''
    <br>
    <p style="font-size: 20px;">
        <strong>Next Step:</strong> Please continue with the <strong>Data Validation Workflow</strong> to see more details on the SHACL Shapes and the Protocol.
    </p>
''', unsafe_allow_html=True)



data_generation_page()