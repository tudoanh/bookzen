import logging
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from bookcrawl.spiders.tiki import TikiSpider
from bookcrawl.spiders.lazada import LazadaSpider
from bookcrawl.spiders.vinabook import VinabookSpider
from bookcrawl.spiders.fahasa import FahasaSpider

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='crawl.log',
    format='%(levelname)s: %(message)s',
    level=logging.WARNING
)


runner = CrawlerProcess(get_project_settings())
runner.crawl(TikiSpider)
runner.crawl(LazadaSpider)
runner.crawl(VinabookSpider)
runner.start()

process = CrawlerProcess({
        'USER_AGENT': 'google-bot',
        })
process.crawl(FahasaSpider)
process.start()
