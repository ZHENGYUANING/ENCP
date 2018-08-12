# -*- coding: utf-8 -*-
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql 
import json 
from scrapy.contrib.exporter import JsonItemExporter,CsvItemExporter
# class JsonPipeline(object):
#     def __init__(self):
#         self.f = open('job1.json','wb')
#         self.exporter = JsonItemExporter(self.f,encoding='utf-8')
#         self.exporter.start_exporting()
#     def process_item(self,item,spider):
#         # if not hasattr(item,'table_name'):
#         #     return item 
#         self.exporter.export_item(item)
#         return item 
#     def close_spider(self,spider):
#         self.exporter.finish_exporting()

# class CsvPipeline(object):
#     def __init__(self):
#         self.f = open('job1.csv','wb+')
#         self.exporter = CsvItemExporter(self.f,encoding='utf-8')
#         self.exporter.start_exporting()

#     def process_item(self,item,spider):
#         if not hasattr(item,'table_name'):
#             return item 
#         self.exporter.export_item(item)
#         return item 
#     def close_spider(self,spider):
#         self.exporter.finish_exporting()

    
class GovPipeline(object):
    def __init__(self):
        self.conn = None 
        self.cur = None 
    def open_spider(self,spider):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root123',
            db = 'clip',
            charset='utf8mb4',
        )
        self.cur = self.conn.cursor()
    def process_item(self, item, spider):

        if not hasattr(item,'table_name'):
            return item
        cols,values = zip(*item.items())
        sql = "INSERT INTO `{}`({})"\
            "VALUE ({}) ON DUPLICATE KEY UPDATE{}".format(
                item.table_name,
                ','.join(['`%s`'% col for col in cols]),
                ','.join(['%s']*len(cols)),
                ','.join('`{}`=%s'.format(col) for col in cols)
            )
        self.cur.execute(sql,values * 2)
        self.conn.commit()
        print(self.cur._last_executed)
        return item 
    def close_spider(self,spider):
        self.cur.close()
        self.conn.close()