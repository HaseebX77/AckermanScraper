# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import re
from html import unescape
from datetime import datetime
import csv
from itemadapter import ItemAdapter

class AckermanPipeline:
    def open_spider(self, spider):
        self.file = open('ackermans_products_clean.csv', 'w', newline='', encoding='utf-8')
        self.exporter = csv.writer(self.file)
        self.exporter.writerow(["SKU", "Title", "Price", "URL", "Images", "Description", "Category", "Color", "Size"])
        self.seen = set()  # avoid duplicates

    def process_item(self, item, spider):
        key = item.get('sku')
        if key not in self.seen:
            self.seen.add(key)
            self.exporter.writerow([
                item.get("sku"),
                item.get("title"),
                item.get("price"),
                item.get("url"),
                ", ".join(item.get("images", [])),
                item.get("description"),
                item.get("category"),
                item.get("color"),
                item.get("size")
            ])
        return item

    def close_spider(self, spider):
        self.file.close()
