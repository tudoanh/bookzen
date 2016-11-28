import logging
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from bookcrawl.spiders.tiki import TikiSpider
from bookcrawl.spiders.lazada import LazadaSpider
from bookcrawl.spiders.vinabook import VinabookSpider

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='crawl.log',
    format='%(levelname)s: %(message)s',
    level=logging.WARNING
)


runner = CrawlerRunner(get_project_settings())
runner.crawl(TikiSpider)
runner.crawl(LazadaSpider)
runner.crawl(VinabookSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()
