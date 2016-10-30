# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from Doubanbook.items import DoubanbookItem
PAGES_RE = re.compile(r"页数:</span> (\d+)<br>")

class BookSpider(CrawlSpider):
    name = 'book'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/',
                  'https://book.douban.com/',]

    rules = (
        Rule(LinkExtractor(allow=r"/subject/\d+/($|\?\w+)"), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'.tag/.*')),   #组合成包含tag的链接
    )

    def parse_item(self, response):
        item = DoubanbookItem()

        item["subject_id"] = int(response.url.split("/")[-2])
        item["type"] = 'book'
        self.get_name(response, item)
        self.get_sub_name(response, item)
        self.get_orig_name(response, item)
        self.get_summary(response, item)
        self.get_authors(response, item)
        self.get_author_intro(response, item)
        self.get_translators(response, item)
        self.get_series(response, item)
        self.get_publisher(response, item)
        self.get_publish_date(response, item)
        self.get_pages(response, item)
        self.get_price(response, item)
        self.get_binding(response, item)
        self.get_isbn(response, item)
        self.get_douban_score(response, item)
        self.get_douban_stars(response, item)
        self.get_douban_votes(response, item)
        self.get_tags(response, item)

        return item

    def get_name(self, response, item):
        name = response.xpath('//title/text()').extract()
        if name: item["name"] = name[0].replace(u'(豆瓣)', '').strip()
    def get_sub_name(self, response, item):
        sub_name = response.xpath('//text()[preceding-sibling::span[text()="副标题:"]][following-sibling::br]').extract()
        if sub_name: item["sub_name"] = sub_name[0]
    def get_orig_name(self, response, item):
        orig_name = response.xpath('//text()[preceding-sibling::span[text()="原作名:"]][following-sibling::br]').extract()
        if orig_name: item["orig_name"] = orig_name[0]
    def get_summary(self, response, item):
        summary = response.xpath('//div[@id="link-report"]//div[@class="intro"]/p/text()').extract()
        if summary: item['summary'] = '\n'.join(i for i in summary)
    def get_authors(self, response, item):
        authors = response.xpath('//a[parent::span[child::span[text()=" 作者"]]]/text()').extract()
        if authors: item["authors"] = authors
    def get_author_intro(self, response, item):
        author_intro = response.xpath('//div[@class="indent "]//div[@class="intro"]/p/text()').extract()
        if author_intro: item['author_intro'] = '\n'.join(i for i in author_intro)
    def get_translators(self, response, item):
        translators = response.xpath('//a[parent::span[child::span[text()=" 译者"]]]/text()').extract()
        if translators: item['translators'] = translators
    def get_series(self, response, item):
        series = response.xpath('//a[preceding-sibling::span[text()="丛书:"]][following-sibling::br]/text()').extract()
        if series: item['series'] = series
    def get_publisher(self, response, item):
        publisher = response.xpath('//text()[preceding-sibling::span[text()="出版社:"]][following-sibling::br]').extract()
        if publisher: item['publisher'] = publisher[0]
    def get_publish_date(self, response, item):
        publish_date = response.xpath('//text()[preceding-sibling::span[text()="出版年:"]][following-sibling::br]').extract()
        if publish_date: item['publish_date'] = publish_date[0]
    def get_pages(self, response, item):
        S = "".join(response.xpath("//div[@id='info']").extract())
        M = PAGES_RE.search(S)
        if M is not None:
            item['pages']  = int(M.group(1))
    def get_price(self, response, item):
        price = response.xpath('//text()[preceding-sibling::span[text()="定价:"]][following-sibling::br]').extract()
        if price: item['price'] = price[0]
    def get_binding(self, response, item):
        binding = response.xpath('//text()[preceding-sibling::span[text()="装帧:"]][following-sibling::br]').extract()
        if binding: item['binding'] = binding[0]
    def get_isbn(self, response, item):
        isbn = response.xpath('//text()[preceding-sibling::span[text()="ISBN:"]][following-sibling::br]').extract()
        if isbn: item['isbn'] = int(isbn[0])
    def get_douban_score(self, response, item):
        douban_score = response.xpath('//strong[@property="v:average"]/text()').extract()
        if douban_score and douban_score[0] != "  ": item['douban_score'] = float(douban_score[0])+0.0
    def get_douban_stars(self, response, item):
        if not item.get('votes', None): return
        xpath = response.xpath('//span[@class="rating_per"]/text()').extract()
        stars = "".join(map(str.strip, xpath)).split("%")[:-1]
        stars = [int(round((float("%.3f" % (float(star) / 100))) * item["vote"])) for star in stars]
        item["douban_stars"] = stars
    def get_douban_votes(self, response, item):
        douban_votes = response.xpath("//span[@property='v:votes']/text()").extract()
        if douban_votes and douban_votes[0] != "  ": item["douban_votes"] = int(douban_votes[0])
    def get_tags(self, response, item):
        T = []
        tags = response.xpath("//div[@id='db-tags-section']//a")
        for tag in tags:
            t = tag.xpath("text()").extract()
            if t: T.append(t[0])
        if T: item["tags"] = T