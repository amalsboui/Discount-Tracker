# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime


class DiscountscraperPipeline:
    def process_item(self, item, spider):

        # Handle name and brand
        raw_name = item.get("name")

        # If name is a list ( brand + name from beautystore )
        if isinstance(raw_name, list) and raw_name:
            item["brand"] = raw_name[0].upper()  # the first element is the brand
            item["name"] = " ".join(raw_name[1:])
        # --- Clean price ---
        raw_price = str(item.get("price")).strip()
        if raw_price:
            try:
                clean_price_str = raw_price.replace("TND", "").replace("\xa0", "").replace(",", ".").strip()
                item["price"] = float(clean_price_str)
            except ValueError:
                item["price"] = 0.0
        else:
            item["price"] = 0.0

        item["link"] = item.get("link", "").strip() if item.get("link") else "No link"

        item["date"] = datetime.now().isoformat()

        return item