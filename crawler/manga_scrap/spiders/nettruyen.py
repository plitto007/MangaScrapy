# Created by [PL]_itto at 4:51 PM 12/29/22
import json
import os

import scrapy
import requests

headers = {
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "authority": "www.nettruyenup.com"
}

COOKIE_PATH = 'nettruyen_cookie'


class NetTruyenSpider(scrapy.Spider):
    name = "nettruyen"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self):
        cookies = load_cookies()
        url = 'https://www.nettruyenup.com/truyen-tranh/imawa-no-kuni-no-alice-70987'
        yield scrapy.Request(url, callback=self.parse, headers=headers, cookies=cookies, meta={
            'handle_httpstatus_list': [403, 503]
        })

    def parse(self, response, **kwargs):
        self.logger.info("Starting parse Manga home page")
        self.logger.info("request: {}".format(response.request.url))
        self.logger.info("status code: {}".format(response.status))
        f = open("response.html", "w")
        f.write(response.text)
        f.close()


def load_cookies():
    # File not exist, return
    if not os.path.isfile(COOKIE_PATH):
        return None

    with open(COOKIE_PATH, 'r') as cookiesfile:
        cookies_str = cookiesfile.read()
        if cookies_str:
            return json.loads(cookies_str)
    return None
