import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()
# ------------------------------
# SQL Connection
# ------------------------------
def get_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )


# ------------------------------
# Function to Run Any SQL Query
# ------------------------------
def run_query(query, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(result)
