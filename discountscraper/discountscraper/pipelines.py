# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def clean_name(brand, name):
    if not brand or not name:
        return name

    brand_clean = brand.strip().upper()
    name_clean = name.strip()

    # Check if name starts with the brand
    if name_clean.upper().startswith(brand_clean):
        # Remove only at the beginning
        name_clean = name_clean[len(brand_clean):].strip()

    return name_clean

class DiscountscraperPipeline:
    def process_item(self, item, spider):

        # Handle name and brand
        raw_name = item.get("name")

        # If name is a list ( brand + name from beautystore )
        if isinstance(raw_name, list) and raw_name:
            item["brand"] = raw_name[0].upper()  # the first element is the brand
            item["name"] = " ".join(raw_name[1:])

        raw_price = str(item.get("price")).strip()
        if raw_price:
            try:
                clean_price_str = raw_price.replace("TND", "").replace("\xa0", "").replace(",", ".").strip()
                item["price"] = float(clean_price_str)
            except ValueError:
                item["price"] = 0.0
        else:
            item["price"] = 0.0

        item["link"] = item.get("link", "").strip() if item.get("link") else "No link"

        item["date"] = datetime.now().isoformat()

        # remove brand from the name for fatales
        item["name"] = clean_name(item.get("brand"), item.get("name"))

        return item

class PostgresPipeline:
    def __init__(self):

        self.conn = psycopg2.connect(
            host = os.getenv("POSTGRES_HOST"),
            dbname = os.getenv("POSTGRES_DB"),
            user = os.getenv("POSTGRES_USER"),
            password = os.getenv("POSTGRES_PASSWORD"),
            port = os.getenv("POSTGRES_PORT")
        )

        self.cur = self.conn.cursor()

        self.cur.execute("""
           CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            brand VARCHAR(50),
            name TEXT,
            price FLOAT,
            date TIMESTAMP,
            link TEXT UNIQUE,
            store VARCHAR(50)
            );
        """)

    def process_item(self, item, spider):
        self.cur.execute("""
            INSERT INTO PRODUCTS (brand, name, price, date, link, store)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,(
            item["brand"],
            item["name"],
            item["price"],
            item["date"],
            item["link"],
            item["store"]
        )
        )

        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

