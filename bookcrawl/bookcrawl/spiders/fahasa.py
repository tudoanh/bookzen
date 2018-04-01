# -*- coding: utf-8 -*-
import datetime
import socket
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request

from unidecode import unidecode
from bookcrawl.items import BooksItem


class FahasaSpider(CrawlSpider):
    name = 'fahasa'
    allowed_domains = ['localhost', 'fahasa.com']
    start_urls = [
        "https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc.html",
        # "https://www.fahasa.com/sach-trong-nuoc/van-hoc-dich.html",
        # "https://www.fahasa.com/sach-trong-nuoc/kinh-te-chinh-tri-phap-ly.html",
        # "https://www.fahasa.com/sach-trong-nuoc/tam-ly-ky-nang-song.html",
        # "https://www.fahasa.com/sach-trong-nuoc/kien-thuc-tong-hop.html",
        # "https://www.fahasa.com/sach-trong-nuoc/khoa-hoc-ky-thuat.html",
        # "https://www.fahasa.com/sach-trong-nuoc/sach-hoc-ngoai-ngu.html",
        # "https://www.fahasa.com/sach-trong-nuoc/phong-thuy-kinh-dich.html",
        # "https://www.fahasa.com/sach-trong-nuoc/nu-cong-gia-chanh.html",
        # "https://www.fahasa.com/sach-trong-nuoc/am-nhac-my-thuat-thoi-trang.html",
        # "https://www.fahasa.com/sach-trong-nuoc/van-hoa-nghe-thuat-du-lich.html"
        # "https://www.fahasa.com/sach-trong-nuoc/lich-su-dia-ly-ton-giao.html",
    ]
    spash_url = 'http://localhost:8050/render.html?url={}&timeout=10&wait=2&images=0'

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        },
        'ROBOTSTXT_OBEY': False,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(self.spash_url.format(url), self.parse)

    def parse(self, response):
        # Get the next page and yield Request
        next_selector = response.xpath('//*[@class="next i-next"]/@href')
        for url in next_selector.extract():
            yield Request(self.spash_url.format(url))

        # Get URL in page and yield Request
        url_selector = response.xpath(
            '//*[@class="product-name p-name-list"]/a/@href')
        for url in url_selector.extract():
            yield Request(self.spash_url.format(url), callback=self.parse_item)

    def parse_item(self, response):
        """
        @url http://localhost:8050/render.html?url=https://www.fahasa.com/pho-pho-pho-co-nha-to.html&timeout=10&wait=1&images=0
        @returns items 1
        @scrapes name name_unidecode price description
        @scrapes url project spider server date
        """
        l = ItemLoader(item=BooksItem(), response=response)

        l.add_value(
            'name', l.get_xpath('//*[@class="product-name"]/h1/text()')[-1]
        )
        l.add_value(
            'name_unidecode',
            unidecode(l.get_xpath('//*[@class="product-name"]/h1/text()')[-1]),
        )
        l.add_value(
            'price',
            l.get_xpath('//*[@class="price"]/text()')[1].strip(),
            TakeFirst(),
            re=r'\d+\.\d+',
        )
        l.add_value(
            'description',
            filter(
                None,
                [
                    re.sub('<[^<]+?>', '', i)
                    for i in l.get_xpath('//*[@class="std"]')
                ],
            ),
            Join('\n'),
        )
        l.add_xpath('image_uri', '//*[@id="image"]/@src')

        # Information fields
        l.add_value('url', response.url[response.url.find('cache:') + 6:])
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()
