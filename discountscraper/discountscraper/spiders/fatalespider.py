import scrapy


class FatalespiderSpider(scrapy.Spider):
    name = "fatalespider"
    allowed_domains = ["www.fatales.tn"]
    start_urls = ["https://www.fatales.tn/promotions"]

    def parse(self, response):
        products = response.css("article.product-miniature")

        for product in products: 

            raw_brand = brand = product.css('h2.product-desc a::text').get()

            raw_name = product.css("h2[itemprop='name'] a.product-name::text").get()
            raw_price = product.css("span.price.product-price::text").get()

            clean_brand = raw_brand.strip() if raw_brand else None
            clean_name = raw_name.strip().title() if raw_name else None
            clean_price = None
            if raw_price:
                # Remove non-digit characters (except comma/dot if decimal)
                price_numbers = ''.join(c for c in raw_price if c.isdigit() or c in [',', '.'])
                # Replace comma with dot for float conversion
                price_numbers = price_numbers.replace(',', '.')
                try:
                    clean_price = float(price_numbers)
                except ValueError:
                    clean_price = None

            yield{
                "brand" : clean_brand,
                "name" : clean_name,
                "price" : clean_price
            }

        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


