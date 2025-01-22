import sqlite3
import os
import pandas as pd
import shutil

uploaded_folder = "uploaded_file"

os.makedirs(uploaded_folder, exist_ok=True)
db_name = "local.db"


def create_database(csv_content):
    csv_file_path = os.path.join(uploaded_folder, csv_content.name)
    with open(csv_file_path, "wb") as file:
        file.write(csv_content.getbuffer())
    print(f"CSV file saved to {csv_file_path}")

    df = pd.read_csv(csv_file_path)

    table_name = os.path.splitext(os.path.basename(csv_content.name))[0]
    # table_name = table_name.replace(" ", "_")  # Replace spaces with underscores

    # Delete existing database if it exists
    delete_local_db(db_name)

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
    return data, table_name


def delete_local_db(directory_path):
    if os.path.exists(directory_path):
        # Iterate over each item in the directory
        if(len(os.listdir(directory_path))>0):

            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                try:
                    # Check if it's a file or directory and remove accordingly
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Delete file or symbolic link
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Delete directory
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
            print(f"All files in {directory_path} have been deleted.")
    else:
        print(f"The directory {directory_path} does not exist.")


def determine_sql_type(series):
    if pd.api.types.is_integer_dtype(series):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(series):
        return "REAL"
    elif pd.api.types.is_bool_dtype(series):
        return "INTEGER"
    else:
        return "TEXT"
