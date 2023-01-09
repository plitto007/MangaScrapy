# Created by [PL]_itto at 4:51 PM 12/29/22
import json
import os

import scrapy
import requests
from ..items import MangaScrapItem, ConvertPDFItem

from ..selenium.sele_nettruyen import open_selenium


class NetTruyenSpider(scrapy.Spider):
    name = "nettruyen"
    manga_name = "Demo"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manga_name = "Alice in borderland"
        self.ready_to_pdf = False

    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse)

    def parse(self, response, **kwargs):
        self.logger.info("Starting parse Manga home page")
        # self.logger.info("request: {}".format(response.request.url))
        # self.logger.info("status code: {}".format(response.status))
        # f = open("response.html", "w")
        # f.write(response.text)
        # f.close()
        url = "https://www.nettruyenup.com/truyen-tranh/imawa-no-kuni-no-alice"
        chapter_data = open_selenium(url, self.manga_name)
        for chapter in reversed(chapter_data):
            self.logger.info("Yield chapter: {}".format(chapter.get("name")))
            if not chapter.get("image_urls"):
                continue
            self.ready_to_pdf = True
            item = MangaScrapItem()
            item['manga_name'] = chapter.get('manga_name')
            item['name'] = chapter.get("name")
            item['file_urls'] = chapter.get("image_urls")
            item['referer'] = url
            item['is_last'] = chapter.get("is_last")
            yield item

    def close(self, spider):
        self.logger.info("CLOSE SPIDER...")
        if self.manga_name and self.ready_to_pdf:
            item = ConvertPDFItem()
            item['manga_name'] = spider.manga_name
