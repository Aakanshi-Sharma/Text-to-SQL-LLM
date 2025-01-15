import os

import streamlit as st
from dotenv import load_dotenv
from sql import create_database
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE-API-KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_response(input, df):
    prompt="""You are SQl query expert, """
    response=model.generate_content([input,df])
    return response.text


st.header("Text To SQL LLM App")
uploaded_file = st.file_uploader("Upload the files", type=["csv"])
if uploaded_file is not None:
    result = create_database(uploaded_file)
    print(result)
