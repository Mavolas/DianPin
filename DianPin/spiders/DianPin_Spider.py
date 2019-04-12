# -*- coding: utf-8 -*-
import scrapy

# 导的包
import re
import requests
import lxml.html

from DianPin.items import DianpinItem
from scrapy.http import Request
from urllib import parse


class DianpinSpider(scrapy.Spider):
    name = 'DianPin_Spider'
    allowed_domains = ['dianping.com']
    start_urls = ['http://www.dianping.com/chengdu/ch10/g102']

    def parse(self, response):
        # node_list = response.xpath("//div[@class='content']//ul//li//div[@class='tit']//h4")

        # 获取列表页所有的链接
        node_list = response.xpath("//*[@id='shop-all-list']/ul/li//div[@class='pic']/a[1]/@href").extract()

        for node in node_list:
            Request(url=node, )

            # item = DianpinItem()
            #
            # yield item;

    # def parse_detail(self, response):




    # title = response.xpath("//div[@class='main']//div[@id='basic-info']//h1[@class='shop-name']/text()").extract()
    #
    # print(title[0])
    #
    # css_url = "http:" + re.search('(//.+svgtextcss.+\.css)', response.text).group()
