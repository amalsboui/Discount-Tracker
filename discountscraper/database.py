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
DB_PORT = 5432

def get_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return conn

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS promotions (
            id SERIAL PRIMARY KEY,
            store VARCHAR(255),
            brand VARCHAR(255),
            name VARCHAR(255),
            price FLOAT,
            link TEXT UNIQUE,
            date_scraped DATE
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Promotions table created successfully!")

from datetime import date

def insert_promotion(store, brand, name, price, link, date=None):
    if date is None:
        date = date.today()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO promotions (store, brand, name, price, link, date_scraped)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (link) DO NOTHING;
    """, (store, brand, name, price, link, date))

    conn.commit()
    cur.close()
    conn.close()

