# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class MangaScrapPipeline:
    def process_item(self, item, spider):
        return item


class NetTruyenImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            print("CRAWL URL: {}".format(image_url))
            yield scrapy.Request(image_url, headers={
                "Referer": item.referer
            })
