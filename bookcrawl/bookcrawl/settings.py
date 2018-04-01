#  -*- coding: utf-8 -*-

#  Scrapy settings for bookcrawl project
#
#  For simplicity, this file contains only settings considered important or
#  commonly used. You can find more settings consulting the documentation:
#
#      http://doc.scrapy.org/en/latest/topics/settings.html
#      http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#      http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'bookcrawl'

SPIDER_MODULES = ['bookcrawl.spiders']
NEWSPIDER_MODULE = 'bookcrawl.spiders'

LOG_LEVEL = 'INFO'

#  Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'bookcrawl (+http://www.yourdomain.com)'
#  USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0"

#  Obey robots.txt rules
ROBOTSTXT_OBEY = True

#  Disable cookies (enabled by default)
COOKIES_ENABLED = True


DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
}

ITEM_PIPELINES = {'bookcrawl.pipelines.MongoPipeline': 900}

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DB = "bookzen"

#  Enable and configure the AutoThrottle extension (disabled by default)
#  See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
#  The initial download delay
AUTOTHROTTLE_START_DELAY = 5
#  The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
#  The average number of requests Scrapy should be sending in parallel to
#  each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
#  Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True
