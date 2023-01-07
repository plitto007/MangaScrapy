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
        url = "https://www.nettruyenup.com/truyen-tranh/imawa-no-kuni-no-alice"
        chapter_data = open_selenium(url)
        for chapter in chapter_data:
            item = MangaScrapItem()
            item['image_urls'] = chapter.get("image_urls")
            item['name'] = chapter.get("name")
            item['referer'] = url
            yield item

    def parse(self, response, **kwargs):
        self.logger.info("Starting parse Manga home page")
        self.logger.info("request: {}".format(response.request.url))
        self.logger.info("status code: {}".format(response.status))
        f = open("response.html", "w")
        f.write(response.text)
        f.close()
