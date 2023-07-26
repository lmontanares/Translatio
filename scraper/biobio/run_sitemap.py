from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from spiders.biobio_sitemap import SiteMapBioBioChile
from datetime import datetime

settings = get_project_settings()
configure_logging(settings)
runner = CrawlerRunner(settings)

sitemap_follow = [
    "2023",
    "2022",
    "2021",
    "2020",
    "2019",
    "2018",
    "2017",
    "2016",
    "2015",
    "2014",
    "2013",
    "2012",
    "2011",
    "2010",
    "2009",
]


@defer.inlineCallbacks
def crawl():
    for follow in sitemap_follow:
        runner.settings[
            "LOG_FILE"
        ] = f"/var/log/translatio-scrapy/scrapy_{datetime.today().strftime('%Y-%m-%d')}.log"
        yield runner.crawl(SiteMapBioBioChile, sitemap_follow=[follow])
        reactor.stop()


crawl()
reactor.run()
