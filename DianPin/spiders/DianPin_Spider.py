# -*- coding: utf-8 -*-
import scrapy


class DianpinSpider(scrapy.Spider):
    name = 'DianPin_Spider'
    allowed_domains = ['dianping.com']
    start_urls = ['http://dianping.com/']

    def parse(self, response):

        node_list = response.xpath("//div[@class='content']//ul//li//div[@class='tit']//h4")

        pass
