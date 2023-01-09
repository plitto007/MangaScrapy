# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MangaScrapItem(scrapy.Item):
    # define the fields for your item here like:
    manga_name = scrapy.Field()
    name = scrapy.Field()
    is_last = scrapy.Field()
    referer = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()


class ConvertPDFItem(scrapy.Item):
    manga_name = scrapy.Field()
