# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from Doubanbook.settings import MONGO_URL, MONGO_DATABASE

class DoubanbookPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri= MONGO_URL,
            mongo_db=MONGO_DATABASE
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name != "book":  return item
        if item.get("subject_id", None) is None: return item

        collection = self.db['book']
        spec = { "subject_id": item["subject_id"] }
        collection.update(spec, {'$set': dict(item)}, upsert=True)

        return None


