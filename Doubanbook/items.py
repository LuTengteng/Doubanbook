# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

#import scrapy
from scrapy import Field, Item

class DoubanbookItem(Item):
    douban_id = Field() #豆瓣图书ID
    type = Field()  #类型
    name = Field()  #标题
    sub_name = Field()  #副标题
    orig_name = Field() #原标题
    summary = Field()   #内容简介
    authors = Field()   #作者
    author_intro = Field()  #作者简介
    translators = Field()   #译者
    series = Field()    #丛书
    publisher = Field() #出版社
    publish_date = Field()  #出版日期
    pages = Field() #页数
    price = Field() #价格
    binding = Field()   #装帧
    isbn = Field()  #ISBN号
    douban_score = Field()  #豆瓣评分
    douban_stars = Field()  #豆瓣5-->1星数量
    douban_votes = Field()  #评分人数
    tags = Field()  #豆瓣标签
