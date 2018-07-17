# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class QuotesPipeline(object):
    def process_item(self, item, spider):
        return item


# https://doc.scrapy.org/en/latest/topics/item-pipeline.html
class MongoPipeline(object):

    def __init__(self, mongo_host, mongo_db):
        self.mongo_host = mongo_host
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
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
