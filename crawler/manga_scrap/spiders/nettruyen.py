# Created by [PL]_itto at 4:51 PM 12/29/22
import scrapy


class NetTruyenSpider(scrapy.Spider):
    name = "nettruyen"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self):
        pass

    def parse(self, response, **kwargs):
        pass
