import sqlite3
import os
import pandas as pd

uploaded_folder = "uploaded_file"

os.makedirs(uploaded_folder, exist_ok=True)


def create_database(csv_content):
    csv_file_path = os.path.join(uploaded_folder, csv_content.name)
    with open(csv_file_path, "wb") as file:
        file.write(csv_content.getbuffer())
    print(f"CSV file saved to {csv_file_path}")

    df = pd.read_csv(csv_file_path)

    db_name = "local.db"
    table_name = os.path.splitext(os.path.basename(csv_content.name))[0]
    table_name = table_name.replace(" ", "_")  # Replace spaces with underscores

    # Delete existing database if it exists
    if os.path.exists(db_name):
        os.remove(db_name)
        print(f"{db_name} deleted.")

    # Create a new SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Dynamically create table schema
    columns_with_types = ', '.join([f'"{col}" {determine_sql_type(df[col])}' for col in df.columns])
    create_table_query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_with_types});'
    cursor.execute(create_table_query)

    # Insert data into the table
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Data from {csv_file_path} inserted into table '{table_name}' in {db_name}.")

    # Commit and close the connection
    conn.commit()
    conn.close()
    data = pd.read_csv(csv_file_path)
    return data


def determine_sql_type(series):
    if pd.api.types.is_integer_dtype(series):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(series):
        return "REAL"
    elif pd.api.types.is_bool_dtype(series):
        return "INTEGER"
    else:
        return "TEXT"
