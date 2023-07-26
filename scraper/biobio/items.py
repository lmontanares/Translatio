# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class BioBioItem(Item):
    url = Field()
    title = Field()
    category = Field()
    date = Field()
    view_count = Field()
