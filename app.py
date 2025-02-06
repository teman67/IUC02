import streamlit as st
from multipage import MultiPage

# Set page configuration here
st.set_page_config(page_title="IUC02", page_icon="🌐", layout="wide")

# load pages scripts
from page_summary import page_summary_body
from data_validation import data_validation_page
# from app_pages.page_LLM import *
# from app_pages.history import *
# from app_pages.page_json_viewer import *
#from app_pages.graph import graph_visualizer_page

app = MultiPage(app_name="IUC02")  # Create an instance of the app

# Add your app pages here using .add_page()
app.add_page("IUC02 Overview", page_summary_body)
app.add_page("Data Validation", data_validation_page)
# app.add_page("Explore Ollama Models", LLM_models)
# app.add_page("Chat History Overview", display_conversation_history)
# app.add_page("JSON File Viewer", json_viewer)
# #app.add_page("Graph Visualizer", graph_visualizer_page)

# page_bg_img = '''
# <style>
# [data-testid="stSidebar"] > div:first-child {
# background-image: url("https://cdn.pixabay.com/photo/2016/01/02/02/36/sky-1117783_1280.jpg");
# background-size: cover;
# }
# </style>
# '''
# st.markdown(page_bg_img, unsafe_allow_html=True)


app.run()  # Run the app