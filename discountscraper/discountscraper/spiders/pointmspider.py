import scrapy
from datetime import datetime
from discountscraper.items import ProductItem
import re
from urllib.parse import urljoin

class PointmspiderSpider(scrapy.Spider):
    name = "pointmspider"
    allowed_domains = ["www.pointm.tn"]
    start_urls = ["https://www.pointm.tn/promotions"]

    def parse(self, response):

        products = response.css("li.ajax_block_product")

        for product in products:
            product_item = ProductItem()
            # Extract brand
            raw_brand = product.css('span.product-manufacturer-name::text').get()
            if not raw_brand:
                raw_brand = product.css('div.right-block-information span::text').get()
            clean_brand = raw_brand.strip().upper() if raw_brand else ""


            # Extract name
            raw_name = product.css("h5 a.product-name::text").get()
            clean_name = raw_name.strip().title() if raw_name else ""

            # Extract raw price (new price)
            raw_price_list = product.css("span.price.product-price *::text").getall()
            raw_price_text = " ".join([x.strip() for x in raw_price_list if x.strip()])
            numbers = re.findall(r"\d+[\.,]?\d*", raw_price_text)
            clean_price = float(numbers[-1].replace(",", ".")) if numbers else 0.0


            # Extract old price
            old_price = product.css("span.old-price.product-price::text").get()
           
            # Calculate Discount
            discount = product.css("span.price-percent-reduction::text").get()

            # Extract product link
            link = product.css("a.product_img_link::attr(href)").get()
            if not link:
                link = product.css("h5 a.product-name::attr(href)").get()

            # Current timestamp
            date = datetime.now().isoformat()

            product_item["brand"] = clean_brand
            product_item["name" ] = clean_name
            product_item["price"] = clean_price
            product_item["old_price"] = old_price
            product_item["discount"] = discount
            product_item["date"] = date
            product_item["link"] = link
            product_item["store"] = "pointm"

            if link:
                yield response.follow(link, callback=self.parse_product_page, meta={'item': product_item})
            else:
                product_item["image"] = None
                yield product_item

        next_page = response.css("li.pagination_next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product_page(self, response):
        product_item = response.meta['item']
        # Extract image from the description page
        image = response.css("div#image-block img::attr(src)").get()
        product_item["image"] = image
        yield product_item




