import scrapy
from datetime import datetime
from discountscraper.items import ProductItem

class FatalespiderSpider(scrapy.Spider):
    name = "fatalespider"
    allowed_domains = ["www.fatales.tn"]
    start_urls = ["https://www.fatales.tn/promotions"]

    def parse(self, response):

        products = response.css("article.product-miniature")

        for product in products:
            product_item = ProductItem()

            product_item["brand"] = product.css('h2.product-desc a::text').get()
            product_item["name" ] = product.css("h2[itemprop='name'] a.product-name::text").get()
            product_item["price"] = product.css("span.price.product-price::text").get()
            product_item["link"] = product.css("h2[itemprop='name'] a.product-name::attr(href)").get()

            yield product_item

        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


