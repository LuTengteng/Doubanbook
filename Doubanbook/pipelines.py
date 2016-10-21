# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from Doubanbook.database import doubanDB

class DoubanbookPipeline(object):

    def process_item(self, item, spider):
        if spider.name != "book":  return item
        if item.get("douban_id", None) is None: return item

        spec = { "douban_id": item["douban_id"] }
        doubanDB.book.update(spec, {'$set': dict(item)}, upsert=True)

        return None


