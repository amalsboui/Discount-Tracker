import scrapy


class BeautystorespiderSpider(scrapy.Spider):
    name = "beautystorespider"
    allowed_domains = ["beautystore.tn"]
    start_urls = ["https://beautystore.tn/promotions"]

    def parse(self, response):
        products = response.css("article.product-miniature")

        
        for product in products: 

            #raw_name_parts gives us brand+name
            raw_name_parts = product.css("h1.h3.product-title a::text").getall()
            raw_price = product.css("span.price::text").get()

            clean_name_full = " ".join([x.strip() for x in raw_name_parts if x.strip()])

            parts = clean_name_full.split(" ", 1)
            clean_brand = parts[0].upper() 
            clean_name = parts[1].title() if len(parts) > 1 else ""

            clean_price_str = raw_price.replace("\xa0", "").replace("TND", "").strip()
            clean_price = float(clean_price_str.replace(",", "."))

            yield{
                "brand" : clean_brand,
                "name" : clean_name,
                "price" : clean_price
            }

        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


