# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AckermanscraperItem(scrapy.Item):
    sku = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    images = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()