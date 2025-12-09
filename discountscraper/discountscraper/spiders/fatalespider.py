import scrapy
from discountscraper.items import ProductItem

class FatalespiderSpider(scrapy.Spider):
    name = "fatalespider"
    allowed_domains = ["www.fatales.tn"]
    start_urls = ["https://www.fatales.tn/promotions"]

    def parse(self, response):

        products = response.css("article.product-miniature")

        for product in products:

            brand = product.css('h2.product-desc a::text').get()
            price = product.css("span.price.product-price::text").get()
            link = product.css("h2[itemprop='name'] a.product-name::attr(href)").get()

            yield response.follow(
                link,
                callback=self.parse_detail,
                meta={
                    "brand": brand,
                    "price": price,
                    "link": link
                }
            )
        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        product_item = ProductItem()

        # scrape the brand + name like this: GOSH MINERAL EYE SHADOW FARD A PAUPIERE
        product_item["name"] = response.css("h1[itemprop=name]::text").get()
        product_item["brand"] = response.meta.get("brand")
        product_item["price"] = response.meta.get("price")
        product_item["link"] = response.meta.get("link")
        product_item["store"] = "fatales"

        yield product_item
