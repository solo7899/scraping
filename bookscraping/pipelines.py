# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscrapingPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        for field_name in adapter.field_names():
            if field_name != "description":
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()

        value = adapter.get("price")
        value = value.replace("£", "")
        adapter["price"] = float(value)

        return item
