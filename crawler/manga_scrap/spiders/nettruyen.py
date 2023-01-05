# Created by [PL]_itto at 4:51 PM 12/29/22
import scrapy
import requests

headers = {
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "authority": "www.nettruyenup.com"
}


class NetTruyenSpider(scrapy.Spider):
    name = "nettruyen"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self):
        url = 'https://www.nettruyenup.com/truyen-tranh/imawa-no-kuni-no-alice-70987'
        yield scrapy.Request(url, callback=self.parse, headers=headers, meta={
            'handle_httpstatus_list': [403, 503]
        })

    def parse(self, response, **kwargs):
        self.logger.info("Starting parse Manga home page")
        self.logger.info("status code: {}".format(response.status))
        f = open("response.html", "w")
        f.write(response.text)
        f.close()
