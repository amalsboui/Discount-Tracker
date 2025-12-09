import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT")
    )
    return conn


def fetch_products(store_name):
    conn = get_db_connection()
    query = "SELECT * FROM products WHERE store = %s ORDER BY date DESC"
    df = pd.read_sql(query, conn, params=(store_name,))
    conn.close()
    return df
