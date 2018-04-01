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

ITEM_PIPELINES = {'bookcrawl.pipelines.MongoPipeline': 900}

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DB = "bookzen"

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
}

#  Enable and configure the AutoThrottle extension (disabled by default)
#  See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = True


# SPLASH settings
SPLASH_URL = 'http://192.168.59.103:8050'

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
