# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from pymongo import MongoClient


class QuotesPipeline(object):
    def process_item(self, item, spider):
        return item


# https://docs.scrapy.org/en/latest/topics/item-pipeline.html#write-items-to-a-json-file
class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('.data/quotes.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        return item


# https://docs.scrapy.org/en/latest/topics/item-pipeline.html#write-items-to-mongodb
class MongoPipeline(object):

    """
    官方文档上的Mongo配置方法仅供参考（可能过时了），新版 pymongo 库不使用 url 配置Mongo连接
    """

    def __init__(self, mongo_host, mongo_db):
        self.mongo_host = mongo_host
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # 这里的配置由 settings.py 文件提供
        # 构造(初始化)方法中的值由这里注入
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = MongoClient(host=self.mongo_host)
        self.db = self.client.get_database(self.mongo_db)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db.get_collection('quote').insert_one(dict(item))
        return item
