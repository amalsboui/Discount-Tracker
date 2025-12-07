import scrapy


class BeautystorespiderSpider(scrapy.Spider):
    name = "beautystorespider"
    allowed_domains = ["beautystore.tn"]
    start_urls = ["https://beautystore.tn/promotions"]

    def parse(self, response):
        products = response.css("article.product-miniature")

        
        for product in products: 

            #getall lel names khatr hashti blbrand wism lproduit 
            #get lel price khatr hashti ken blprice baad discount 
            raw_name = product.css("h1.h3.product-title a::text").getall()
            raw_price = product.css("span.price::text").get()

            clean_name = " ".join([x.strip() for x in raw_name if x.strip()])
            clean_price = raw_price.replace("\xa0", "").strip() if raw_price else None

            yield{
                "name" : clean_name,
                "price" : clean_price
            }

        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


