# -*- coding: utf-8 -*-
import scrapy

# 导的包
import re
import requests
import lxml.html


class DianpinSpider(scrapy.Spider):
    name = 'DianPin_Spider'
    allowed_domains = ['dianping.com']
    start_urls = ['http://www.dianping.com/shop/98531630/']

    def parse(self, response):
        # node_list = response.xpath("//div[@class='content']//ul//li//div[@class='tit']//h4")

        title = response.xpath("//div[@class='main']//div[@id='basic-info']//h1[@class='shop-name']/text()").extract()

        print(title[0])

        css_url = "http:" + re.search('(//.+svgtextcss.+\.css)', response.text).group()

        result = requests.get(
            'https://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/2416ff021a8fccb10b15e20ca8d5711c.svg')
        tree = lxml.html.fromstring(result.content)

        a = tree.xpath('//text[@y="36"]/text()')[0]
        b = tree.xpath('//text[@y="78"]/text()')[0]
        c = tree.xpath('//text[@y="127"]/text()')[0]
        d = tree.xpath('//text[@y="172"]/text()')[0]



        "//div[@class='main']//div[@id='basic-info']//p[@class='expand-info tel']"

        # x ,y 是得到的两个坐标点
        # 调用上面的函数
        x, y = css_info('eua80')[0]
        x, y = int(x), int(y)
        print('坐标', x, y)
        if y <= 41:
            print('数字：', a[x // 14])
        elif y <= 88:
            print('数字：', b[x // 14])
        elif y <= 127:
            print('数字：', c[x // 14])
        else:
            print('数字：', d[x // 14])
        pass


# 获取css页面的详情信息，用正则匹配得到css的定位数据
def css_info(info):
    # css 页面   这个网址是会变化的，修改为自己获取到的
    css_html = requests.get(
        'https://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/29e76c3da845ca8b35251e24d615703a.css').text
    # mty2pe{background:-180.0px -1664.0px;}
    # 正则，这里有个坑，刚开始使用+拼接，不能匹配
    str_css = r'%s{background:-(\d+).0px -(\d+).0px' % info
    css_re = re.compile(str_css)
    info_css = css_re.findall(css_html)
    # print(css_html)
    # print(str_css)
    # print(info_css)
    return info_css
