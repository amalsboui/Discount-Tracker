import scrapy
from datetime import datetime
from discountscraper.items import ProductItem

class FatalespiderSpider(scrapy.Spider):
    name = "fatalespider"
    allowed_domains = ["www.fatales.tn"]
    start_urls = ["https://www.fatales.tn/promotions"]

    def parse(self, response):

        products = response.css("article.product-miniature")
        product_item = ProductItem()

        for product in products: 
            # Extract brand 

            raw_brand = brand = product.css('h2.product-desc a::text').get()
            clean_brand = raw_brand.strip() if raw_brand else ""

            # Extract name
            raw_name = product.css("h2[itemprop='name'] a.product-name::text").get()
            clean_name = raw_name.strip().title() if raw_name else ""

            # Extract price and convert to float
            raw_price = product.css("span.price.product-price::text").get()
            clean_price = float(raw_price.replace("TND", "").replace("\xa0", "").replace(",", ".").strip()) if raw_price else 0.0
 
             # Extract product link
            link = product.css("h2[itemprop='name'] a.product-name::attr(href)").get()

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


