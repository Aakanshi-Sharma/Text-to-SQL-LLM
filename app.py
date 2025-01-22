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
    prompt = f"""You are an SQL query expert. Given a dataset, generate a valid SQL query based on the user's input query (No PREAMBLE only query).
        Dataset Schema:
        {df.head().to_string(index=False)}
        User Query: {input}
        SQL Query:"""
    try:
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"


def sql_response(db_name, query, table):
    conn = sqlite3.connect(db_name)
    query = query.replace("```sql", "").replace("```", "").strip()
    query = query.replace("dataset", table)
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data


st.header("Text To SQL LLM App")
uploaded_file = st.file_uploader("Upload the files", type=["csv"])
if uploaded_file is not None:
    result, table_name = create_database(uploaded_file)
    user_query = st.text_input("Enter the query")
    submit_button = st.button("Submit")

    if submit_button:
        with st.spinner('Wait for it...'):
            response = generate_response(user_query, result)
            st.code(response)
            query_result = sql_response("local.db", response, table_name)
            if isinstance(query_result, pd.DataFrame):
                st.write("Query Result:")
                st.write(query_result)
            else:
                st.error(query_result)
