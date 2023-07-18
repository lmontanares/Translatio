from scrapy.spiders import SitemapSpider
from scrapy.http import Request, Response
import re
from biobio.items import BioBioItem


class SiteMapBioBioChile(SitemapSpider):
    name = "biobiochile_sitemap"
    allowed_domains = ["biobiochile.cl"]
    sitemap_urls = ["https://www.biobiochile.cl/static/sitemap.xml"]
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
    sitemap_rules = [
        (r"/noticias/", "parse"),
    ]
    custom_settings = {"REDIRECT_ENABLED": True}
    sitemap_alternate_links = True

    def parse(self, response: Response):
        self.logger.info(
            f"[Translatio] Parse function called on {response.url}"
        )
        item = BioBioItem()
        item["url"] = response.url
        # item["title"] = response.css("title::text").get()
        item["title"] = response.css("title::text").get().strip()
        regex = re.search(r"(\D*)(/\d{4}/\d{2}/\d{2})", response.url)
        item["category"] = "/".join(regex.group(1).split("/")[3:])
        item["date"] = regex.group(2)[1:]
        id_value = response.xpath("//article/@data-id").get()
        api_url = f"https://contador.biobiochile.cl/api/visitas/get-visitas?idNota={id_value}"
        request = Request(url=api_url, callback=self.parse_api_response)
        request.meta["item"] = item
        yield request

    def parse_api_response(self, response):
        item = response.meta["item"]
        # item["view_count"] = response.text
        item["view_count"] = response.text.split(":")[-1][:-2]
        self.logger.info(f"[Translatio] Item Parsed: {item}")
        yield item
