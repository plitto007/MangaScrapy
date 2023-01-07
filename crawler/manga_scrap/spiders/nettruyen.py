# Created by [PL]_itto at 4:51 PM 12/29/22
import json
import os

import scrapy
import requests
from ..items import MangaScrapItem

from ..selenium.sele_nettruyen import open_selenium


class NetTruyenSpider(scrapy.Spider):
    name = "nettruyen"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        chapter_data = open_selenium(url)
        for chapter in reversed(chapter_data):
            self.logger.info("Yield chapter: {}".format(chapter.get("name")))
            if not chapter.get("image_urls"):
                continue
            item = MangaScrapItem()
            item['name'] = chapter.get("name")
            item['file_urls'] = chapter.get("file_urls")
            item['referer'] = url
            yield item
