# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewscastItem(scrapy.Item):
    # define the fields for your item here like:
    source = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    timestamp = scrapy.Field()
    category = scrapy.Field()
    country = scrapy.Field()
    hash = scrapy.Field()
