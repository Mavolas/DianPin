# -*- coding: utf-8 -*-
import scrapy

# 导的包
import re
import requests
import lxml.html

from DianPin.items import DianpinItem
from scrapy.http import Request
from urllib import parse
from fake_useragent import UserAgent


class DianpinSpider(scrapy.Spider):
    name = 'DianPin_Spider'
    allowed_domains = ['dianping.com']
    start_urls = ['http://www.dianping.com/chengdu/ch10/g219r1591']

    def parse(self, response):
        # node_list = response.xpath("//div[@class='content']//ul//li//div[@class='tit']//h4")

        # 获取列表页所有的链接
        node_list = response.xpath("//*[@id='shop-all-list']/ul/li//div[@class='pic']/a[1]/@href").extract()

        for node in node_list:
            yield Request(url=node, callback=self.parse_detail)

        #提取下一页
        next_url = response.xpath("//div[@class='page']//a[@class='next']/@href").extract_first("")
        if next_url:
            yield Request(url=next_url,callback=self.parse)

    def parse_detail(self, response):

        dianpin_item = DianpinItem()

        title = response.xpath("//div[@id='basic-info']//h1[@class='shop-name']/text()").extract()[0]
        star = response.xpath("//*[@id='basic-info']/div[1]/span[1]/@title").extract()[0]

        # 获取svg表格中被替换的数据
        def get_hide_char(x, y, type, url):
            response = requests_middler(url)
            html = lxml.html.fromstring(response.content)
            # 网页格式是否有defs元素
            if len(html.xpath('//defs//path/@d')) < 1:  # 如果没有defs标签
                hight = html.xpath('//text/@y')
                hight.append(y)
                hight = sorted(hight, key=lambda i: int(i))
                y = hight.index(y)
                # 若纵坐标与标签y相等相等时，取同行的高度
                if y != len(hight) - 1 and hight[y] == hight[y + 1]:
                    y = y + 1
                content = html.xpath('//text/text()')[y]
                content = ''.join(content).strip()
                x = int(int(x) / 14)
                return content[x]
            else:  # 如果含有defs标签
                hight = html.xpath('//defs//path/@d')
                hight = [i.replace('M0', '').replace('H600', '').strip() for i in hight]
                hight.append(y)
                hight = sorted(hight, key=lambda i: int(i))
                y = hight.index(y)
                # 若hight相等时，取同行的高度
                if y != len(hight) - 1 and hight[y] == hight[y + 1]:
                    y = y + 1
                content = html.xpath('//textpath/text()')[y]
                content = ''.join(content).strip()
                x = int(int(x) / 14)
                return content[x]

        # 请求url统一方式
        def requests_middler(url):

            ua = UserAgent()
            headers = {'User-Agent': ua.random}
            html = requests.get(url, headers=headers)
            return html

        # 获取css表中key值对应的坐标，以及标签对应svg表链接
        def get_position_xy(html, password, type, url):
            # 获取key值对应的坐标
            rule = re.compile(password + '{background:-(.*?).0px -(.*?).0px;')
            result = re.findall(rule, html)[0]
            x = result[0]
            y = result[1]
            # 获取标签所对应的svg表格
            rule = re.compile(type + '\[class\^="\w+"\]\{(.*?)}', re.S)
            result = re.findall(rule, html)[0]
            rule = re.compile('url\((.*?)\)')
            href = re.findall(rule, result)
            url = 'http:' + href[0]
            hide_char = get_hide_char(x, y, type, url)
            return hide_char

        # 解密前数据做好清洗，清洗成标签与文字组成的list，保证还原字符串顺序
        def get_hide_string(s, url):
            result = []
            a_list = re.split('</\S+>', s)
            # print(a_list)
            b = []
            for i in a_list:
                try:
                    dex = i.index('<')
                except ValueError:
                    b.append(i)
                    continue
                if dex != 0:
                    b.append(i[:dex])
                rule = re.compile('<(.*?) class="(.*?)"')
                tag = re.findall(rule, i[dex:])[0]
                b.append(tag)
            try:
                b.remove('')
            except ValueError:
                pass
            print(b)  # b为已清洗好的list，接下来分别还原标签替换数据
            html = requests_middler(url)
            html = html.text
            for tag in b:
                # 遇到类别标签则分类进行筛选
                if tag[0] == 'span' or tag[0] == 'cc' or tag[0] == 'bb' or tag[0] == 'd':
                    hide_char = get_position_xy(html, tag[1], tag[0], url)
                    result.append(hide_char)
                # 防止被其它标签干扰
                elif tag[0] == '' or tag[0] == 'p' or tag[0] == 'div':
                    continue
                # 遇到中文及不含标签则直接加入list
                else:
                    result.append(tag)
            return ''.join(result).strip('\n').strip()

        html = lxml.html.fromstring(response.text)
        # 找到标签数据，必须要保留标签，这里以商店地址为例
        rule = re.compile('<p class="expand-info tel">(.*?)</p>', re.S)
        address = re.findall(rule, response.text)[0]
        address = address.strip().replace('\n', '').replace('&nbsp', '')
        address = address.replace('<span class="info-name">电话：</span>', "")
        # 找到css表，css表链接存放位置固定，所以直接获取
        css = html.xpath('//link[@rel="stylesheet"]/@href')[1]
        url = 'http:' + css.strip()
        result = get_hide_string(address, url)
        result = result.replace(' ', '')

        print(title)
        print('解密前数据：' + address)
        print('解密后数据：' + result)

        dianpin_item["id"] = title
        dianpin_item["name"] = title
        dianpin_item["phone"] = result
        dianpin_item["star"] = star

        yield dianpin_item
        
        # dianpin_item["phone"] = result

