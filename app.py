import streamlit as st
from sql import create_database

st.header("Text To SQL LLM App")
uploaded_file = st.file_uploader("Upload the files", type=["csv"])
if uploaded_file is not None:
    result = create_database(uploaded_file)
    print(result)
