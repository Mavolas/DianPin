# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    area = scrapy.Field()
    type = scrapy.Field()
    name = scrapy.Field()
    star = scrapy.Field()
    phone = scrapy.Field()
    commentCount = scrapy.Field()
    address = scrapy.Field()


