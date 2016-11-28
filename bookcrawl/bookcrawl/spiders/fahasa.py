# -*- coding: utf-8 -*-
import datetime
import socket
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from unidecode import unidecode
from bookcrawl.items import BooksItem


class FahasaSpider(CrawlSpider):
    name = 'fahasa'
    allowed_domains = ['fahasa.com']
    start_urls = [
            "http://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc.html",
            "http://www.fahasa.com/sach-trong-nuoc/van-hoc-dich.html",
            "http://www.fahasa.com/sach-trong-nuoc/kinh-te-chinh-tri-phap-ly.html",
            "http://www.fahasa.com/sach-trong-nuoc/tam-ly-ky-nang-song.html",
            "http://www.fahasa.com/sach-trong-nuoc/kien-thuc-tong-hop.html",
            "http://www.fahasa.com/sach-trong-nuoc/khoa-hoc-ky-thuat.html",
            "http://www.fahasa.com/sach-trong-nuoc/tu-dien.html",
            "http://www.fahasa.com/sach-trong-nuoc/sach-hoc-ngoai-ngu.html",
            "http://www.fahasa.com/foreigncategory.html",
            ]

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//*[@title="Next"]')),
        Rule(LinkExtractor(
            restrict_xpaths='//*[@class="product-name p-name-list"]/a'),
            callback='parse_item'),
    )

    def parse_item(self, response):
        """
        @url http://www.fahasa.com/luat-im-lang-mario-puzo.html
        @returns items 1
        @scrapes name name_unidecode price description
        @scrapes url project spider server date
        """
        l = ItemLoader(item=BooksItem(), response=response)

        l.add_value('name', l.get_xpath('//*[@class="product-name"]/h1/text()')[-1])
        l.add_value('name_unidecode', unidecode(l.get_xpath('//*[@class="product-name"]/h1/text()')[-1]))
        l.add_xpath('price', '//*[@class="price-box"]/p[1]/span[2]/text()', TakeFirst(), re=r'\d+\.\d+')
        l.add_value('description',
                    filter(None,
                        [re.sub('<[^<]+?>', '', i) for i in l.get_xpath('//*[@class="std"]')]),
                    Join('\n'))
        l.add_xpath('image_uri', '//*[@id="image"]/@src')

        # Information fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()
