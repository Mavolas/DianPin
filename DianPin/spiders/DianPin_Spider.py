# -*- coding: utf-8 -*-
import scrapy


class DianpinSpiderSpider(scrapy.Spider):
    name = 'DianPin_Spider'
    allowed_domains = ['dianping.com']
    start_urls = ['http://dianping.com/']

    def parse(self, response):
        pass
