# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib.parse import urlparse

import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline


class MangaScrapPipeline:
    def process_item(self, item, spider):
        spider.logger.info("process item : {}".format(item))
        return item


class NetTruyenImagesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        print("request: {}".format(request.url))
        print('files/' + os.path.basename(urlparse(request.url).path))
        print("ITEM: {}".format(item))
        print('****')
        return 'files/' + os.path.basename(urlparse(request.url).path)

    def get_media_requests(self, item, info):
        # urls = ItemAdapter(item).get(self.images_urls_field, [])
        # return [scrapy.Request(u, headers={
        #     "Referer": item['referer']
        # }) for u in urls]
        requests = []
        for image_url in item['file_urls']:
            print("CRAWL URL: {}".format(image_url))
            requests.append(scrapy.Request(image_url, headers={
                "Referer": item['referer']
            }))
        return requests
