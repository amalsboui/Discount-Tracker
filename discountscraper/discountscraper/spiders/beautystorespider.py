import scrapy
from datetime import datetime
from discountscraper.items import ProductItem
from database import insert_store, insert_promotion



class BeautystorespiderSpider(scrapy.Spider):
    name = "beautystorespider"
    allowed_domains = ["beautystore.tn"]
    start_urls = ["https://beautystore.tn/promotions"]

    def parse(self, response):
        products = response.css("article.product-miniature")
        product_item = ProductItem()

        for product in products:

            # Extract brand and name
            raw_name_parts = product.css("h1.h3.product-title a::text").getall()
            clean_name_full = " ".join([x.strip() for x in raw_name_parts if x.strip()])

            parts = clean_name_full.split(" ", 1)
            clean_brand = parts[0].upper() 
            clean_name = parts[1].title() if len(parts) > 1 else ""

            # Extract price and convert to float
            raw_price = product.css("span.price::text").get()
            clean_price_str = raw_price.replace("\xa0", "").replace("TND", "").strip()
            clean_price = float(clean_price_str.replace(",", "."))

            # Extract product link
            link = product.css("h1.h3.product-title a::attr(href)").get()

            # Current timestamp
            date = datetime.now().isoformat()

            product_item["brand"] = clean_brand
            product_item["name" ] = clean_name
            product_item["price"] = clean_price
            product_item["date"] = date
            product_item["link"] = link

            yield product_item

        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


