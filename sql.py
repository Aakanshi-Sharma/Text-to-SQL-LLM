import sqlite3
import os
import pandas as pd
from io import StringIO

db_name = "local.db"


def create_database(csv_content):
    csv_file = StringIO(csv_content)
    df = pd.read_csv(csv_file)
    table_name = os.path.basename(csv_content.name)
    if os.path.exists(db_name):
        os.remove(db_name)

    conn = sqlite3.connect("local.db")
    cursor = conn.cursor()
    columns_with_types = ', '.join([f'"{col}" {determine_sql_type(df[col])}' for col in df.columns])
    create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types});'
    cursor.execute(create_table_query)
    df.to_sql(table_name, conn, if_exists="append", index=False)
    conn.commit()
    conn.close()
    return True


def determine_sql_type(series):
    if pd.api.types.is_integer_dtype(series):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(series):
        return "REAL"
    elif pd.api.types.is_bool_dtype(series):
        return "INTEGER"
    else:
        return "TEXT"
