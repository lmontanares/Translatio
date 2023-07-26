import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, Response
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from biobio.items import BioBioItem


class BioBioCrawlSpider(CrawlSpider):
    name = "biobio_crawler"
    allowed_domains = ["biobiochile.cl"]
    start_urls = ["https://www.biobiochile.cl"]
    rules = (
        Rule(
            LinkExtractor(
                allow=(r"/noticias/",),
            ),
            callback="parse_items",
            follow=True,
        ),
    )

    def parse_category(self, response: Response):
        # TODO: Implement this function
        pass

    def parse_items(self, response: Response):
        self.logger.info(
            f"[Translatio] Parse function called on {response.url}"
        )
        item = BioBioItem()
        item["url"] = response.url
        item["title"] = response.css("title::text").get().strip()
        regex = re.search(r"(\D*)(/\d{4}/\d{2}/\d{2})", response.url)
        item["category"] = "/".join(regex.group(1).split("/")[3:])
        item["date"] = regex.group(2)[1:]
        id_value = response.xpath("//article/@data-id").get()
        api_url = f"https://contador.biobiochile.cl/api/visitas/get-visitas?idNota={id_value}"
        request = Request(url=api_url, callback=self.parse_api_response)
        request.meta["item"] = item
        yield request

    def parse_api_response(self, response: Response):
        item: BioBioItem = response.meta["item"]
        item["view_count"] = response.text.split(":")[-1][:-2]
        self.logger.info(f"[Translatio] Scraped Item: {item}")
        yield item
