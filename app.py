import os
import sqlite3

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sql import create_database
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE-API-KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_response(input, df):
    prompt = f"""You are an SQL query expert. Given a dataset, generate a valid SQL query based on the user's input query.
        Dataset Schema:
        {df.head().to_string(index=False)}
        User Query: {input}
        SQL Query:"""
    try:
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"


def sql_response(db_name, query):
    conn = sqlite3.connect(db_name)
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data


st.header("Text To SQL LLM App")
uploaded_file = st.file_uploader("Upload the files", type=["csv"])
if uploaded_file is not None:
    result = create_database(uploaded_file)
    user_query = st.text_input("Enter the query")
    submit_button = st.button("Submit")

    if submit_button:
        with st.spinner('Wait for it...'):
            result = generate_response(user_query, result)
            st.code(result)
            query_result = sql_response("local.db", result)
            if isinstance(query_result, pd.DataFrame):
                st.write("Query Result:")
                st.write(query_result)
            else:
                st.error(query_result)
