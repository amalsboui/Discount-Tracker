import scrapy
from datetime import datetime
from discountscraper.items import ProductItem

class BeautystorespiderSpider(scrapy.Spider):
    name = "beautystorespider"
    allowed_domains = ["beautystore.tn"]
    start_urls = ["https://beautystore.tn/promotions"]

    def parse(self, response):
        products = response.css("article.product-miniature")

        for product in products:
            product_item = ProductItem()

            product_item["name" ] = product.css("h1.h3.product-title a::text").getall()
            product_item["price"] = product.css("span.price::text").get()
            product_item["link"] = product.css("h1.h3.product-title a::attr(href)").get()

            yield product_item

        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


