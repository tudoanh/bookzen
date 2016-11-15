import logging
from twisted.internet import reactor
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from bookcrawl.spiders.tiki import TikiSpider
from bookcrawl.spiders.lazada import LazadaSpider
from bookcrawl.spiders.vinabook import VinabookSpider

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='crawl.log',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


runner = CrawlerRunner()
runner.crawl(TikiSpider)
runner.crawl(LazadaSpider)
runner.crawl(VinabookSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()
