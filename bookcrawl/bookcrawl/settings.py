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

SPLASH_URL = 'http://localhost:8050/'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

#  Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'bookcrawl (+http://www.yourdomain.com)'
#  USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0"

#  Obey robots.txt rules
ROBOTSTXT_OBEY = True

#  Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

#  Configure a delay for requests for the same website (default: 0)
#  See http://scrapy.readthedocs.org/en/latest/topics/settings.html# download-delay
#  See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
#  The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

#  Disable cookies (enabled by default)
COOKIES_ENABLED = True
SPLASH_COOKIES_DEBUG = False

#  Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

#  Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#    'Accept-Language': 'en',
# }

#  Enable or disable spider middlewares
#  See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

#  Enable or disable downloader middlewares
#  See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#     'bookcrawl.middlewares.MyCustomDownloaderMiddleware': 543,
# }
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
}

#  Enable or disable extensions
#  See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#     'scrapy.extensions.telnet.TelnetConsole': None,
# }

#  Configure item pipelines
#  See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     'bookcrawl.pipelines.SomePipeline': 300,
# }
ITEM_PIPELINES = {'bookcrawl.pipelines.MongoPipeline': 900, }

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

#  Enable and configure HTTP caching (disabled by default)
#  See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html# httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
