# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from os import scandir
from urllib.parse import urlparse

import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from scrapy.settings import Settings
import glob
from fpdf import FPDF
from PIL import Image
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class MangaScrapPipeline:
    def process_item(self, item, spider):
        spider.logger.info("process item : {}".format(item))
        return item


class NetTruyenImagesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        print('Downloading files/' + os.path.basename(urlparse(request.url).path))
        return '{}/{}/'.format(item['manga_name'], item['name']) + os.path.basename(urlparse(request.url).path)

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

    def item_completed(self, results, item, info):
        print("=======================")
        print("item downloaded: {}".format(results))
        print("info: {}".format(info))
        print("item: {}".format(item))
        print("=======================")
        if item['is_last']:
            self.convert_2_pdf(item['manga_name'])

    def convert_2_pdf(self, manga_name):
        """
        Convert  images downloaded to pdf
        """
        print("***********CONVERT 2 PDF******************")
        try:
            pdf = FPDF(format='letter')
            download_folder = "{}/{}/".format(settings.get("FILES_STORE"), manga_name)
            print('downloaded folder: {}'.format(download_folder))
            entries = sorted(os.listdir(download_folder))
            # iterating each chapter folder
            for chapter_path in entries:
                print('chapter path {}'.format(chapter_path))
                if os.path.isdir(download_folder + "/" + chapter_path):
                    chapter_files_path = sorted(os.listdir(download_folder + "/" + chapter_path))
                    for chapter_img in chapter_files_path:
                        print("{} == FILE DATA: {}".format(type(chapter_img), chapter_img))
                        # pdf.add_page()
                        #
                        # pdf.image(download_folder + "/" + chapter_path + '/' + chapter_img)
                        imageFile = download_folder + "/" + chapter_path + '/' + chapter_img
                        cover = Image.open(imageFile)
                        width, height = cover.size

                        # convert pixel in mm with 1px=0.264583 mm
                        width, height = float(width * 0.264583), float(height * 0.264583)

                        # given we are working with A4 format size
                        pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}

                        # get page orientation from image size
                        orientation = 'P' if width < height else 'L'

                        #  make sure image size is not greater than the pdf format size
                        width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
                        height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']

                        pdf.add_page(orientation=orientation)

                        pdf.image(imageFile, 0, 0, width, height)

            pdf.output("{}.pdf".format(manga_name), "F")
        except Exception as e:
            print("Error: ")
            print(e)
