# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DiscountscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class ProductItem(scrapy.Item):
    brand = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    discount = scrapy.Field()
    image = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()
    store = scrapy.Field()

