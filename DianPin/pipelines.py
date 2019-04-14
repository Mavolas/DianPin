# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from openpyxl import Workbook

# json
class DianpinPipeline(object):

    def __init__(self):
        self.f = open("tencent.json", "w",encoding="utf-8")

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + ",\n"

        self.f.write(content)

        return item

    def close_spider(self, spider):
        self.f.close()


class ExcelPipeline(object):

    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active

        self.ws.append(['id','area','type','name','star','phone','commentCount','address'])

    def process_item(self, item, spider):

        line = [item['id'],item['area'],item['type'],item['name'],item['star'],item['phone'],item['commentCount'],item['address']]
        self.ws.append(line)
        self.wb.save('DianPin.xlsx')
        return item