# -*- coding: utf-8 -*-
import datetime
import socket
import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from unidecode import unidecode
from bookcrawl.items import BooksItem


class VinabookSpider(CrawlSpider):
    name = 'vinabook'
    allowed_domains = ['www.vinabook.com']
    start_urls = [
            "https://www.vinabook.com/c348/sach-kinh-te/page-1/",
            "https://www.vinabook.com/c739/sach-ngoai-van/page-1/",
            "https://www.vinabook.com/c353/van-hoc-trong-nuoc/page-1",
            "https://www.vinabook.com/c354/van-hoc-nuoc-ngoai/page-1",
            "https://www.vinabook.com/c671/sach-thuong-thuc-doi-song/page-1",
            "https://www.vinabook.com/c668/sach-phat-trien-ban-than/page-1",
            "https://www.vinabook.com/c670/sach-chuyen-nganh/page-1",
            ]

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//*[@rel="next"]')),
        Rule(LinkExtractor(
            restrict_xpaths='//*[@class="product_thumb"]'),
            callback='parse_item'),
    )

    def parse_item(self, response):
        """
        @url https://www.vinabook.com/lam-quen-thong-ke-hoc-qua-biem-hoa-p71348.html
        @returns items 1
        @scrapes name name_unidecode price description
        @scrapes url project spider server date
        """
        l = ItemLoader(item=BooksItem(), response=response)

        l.add_value('name', l.get_xpath('//*[@itemprop="title"]/text()')[-1])
        l.add_value('name_unidecode', unidecode(l.get_xpath('//*[@itemprop="title"]/text()')[-1]))
        l.add_xpath('price', '//*[contains(@id, "discounted_price")]/span/text()', TakeFirst())
        l.add_xpath('author', '//*[@itemprop="author"]/text()')
        l.add_value('description',
                    filter(None,
                        [re.sub('<[^<]+?>', '', i) for i in l.get_xpath('//*[@class="full-description"]/p')]),
                    Join('\n'))
        l.add_xpath('image_uri', '//*[@itemprop="image"]/@src')

        # Information fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()
