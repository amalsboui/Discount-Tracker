import psycopg2
import os
from psycopg2 import sql
from datetime import date
from dotenv import load_dotenv

load_dotenv()

DB_HOST = "localhost"
DB_NAME = "discounts_db"
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = 5433

def get_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return conn
