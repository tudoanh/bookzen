# -*- coding: utf-8 -*-
import datetime
import scrapy
import socket
import urlparse
import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.http import Request

from unidecode import unidecode
from bookcrawl.items import BooksItem


class TikiSpider(scrapy.Spider):
    name = "tiki"
    allowed_domains = ["tiki.vn"]
    start_urls = [
            "https://tiki.vn/sach-kinh-te/c846",
            "https://tiki.vn/sach-van-hoc/c839",
            "https://tiki.vn/sach-ky-nang-song-dep/c870",
            "https://tiki.vn/sach-nuoi-day-con/c2527",
            "https://tiki.vn/sach-kien-thuc-tong-hop/c873",
            "https://tiki.vn/chinh-tri-phap-ly/c875",
            "https://tiki.vn/tam-ly-gioi-tinh/c868",
            "https://tiki.vn/sach-teen/c714",
            "https://tiki.vn/fiction-literature/c9",
            "https://tiki.vn/how-to-advice/c614",
            "https://tiki.vn/teens/c31",
            "https://tiki.vn/memoirs-biographies/c15",
            "https://tiki.vn/business-investing/c4",
            "https://tiki.vn/culture-and-art/c623",
            ]

    mc = MapCompose(lambda i: urlparse.urljoin('http://tiki.vn', i))

    def parse(self, response):
        # Get the next page and yield request
        next_selector = response.xpath(
                '//*[@class="next"]/@href')
        for url in next_selector.extract():
            yield Request(self.mc(url)[0])

        # Get URL in page and yield Request
        url_selector = response.xpath(
                '//*[@class="product-item   "]/a/@href')
        for url in url_selector.extract():
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        """
        @url https://tiki.vn/hieu-ng-canh-buom-p146105.html
        @returns items 1
        @scrapes name name_unidecode price description
        @scrapes url project spider server date
        """
        l = ItemLoader(item=BooksItem(), response=response)

        l.add_xpath('name', '//*[@class="item-name"]/text()', MapCompose(unicode.strip, unicode.title))
        l.add_xpath('name_unidecode', '//*[@class="item-name"]/text()', MapCompose(unidecode, str.strip, str.title))
        l.add_xpath('author', '//*[@class="item-brand"]/p/a/text()')
        l.add_xpath('price', '//*[@id="span-price"]/text()', TakeFirst(), re=r'\d+\.\d+')
        l.add_value('description',
                    [re.sub('<[^<]+?>', '', i) for i in l.get_xpath('//*[@id="gioi-thieu"]/p')],
                    Join('\n'))
        l.add_xpath('image_uri', '//*[@itemprop="image"]/@src')

        # Information fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()
