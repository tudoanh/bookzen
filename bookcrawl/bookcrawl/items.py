# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class BooksItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    name_unidecode = Field()
    author = Field()
    description = Field()
    price = Field()
    image_uri = Field()

    # Information fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()
