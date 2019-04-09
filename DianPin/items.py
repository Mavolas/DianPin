# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    star = scrapy.Field()
    commentCount = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    taste = scrapy.Field()
    environ = scrapy.Field()
    service = scrapy.Field()

    pass
