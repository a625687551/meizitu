# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from meizitu.items import MeizituItem
from meizitu import settings
from scrapy import Request
from pymongo import MongoClient
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class MeizituPipeline(object):
    def process_item(self, item, spider):
        return item


class DownloadImagesPipeline(ImagesPipeline):
    '''
    对图片的下载包括命名和下载存放地址
    '''

    def get_media_requests(self, item, info):  # 下载图片
        for image_url in item['image_url']:
            yield Request(image_url, meta={'item': item})

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        # image_name=request
        # file_paths=item['file_paths']
        if not file_paths:
            raise DropItem(u'图片未下载好{}'.format(file_paths))
        item['file_paths'] = file_paths
        return item

    def file_path(self, request, response=None, info=None):  # 通过这个来对图片进行命名
        item = request.meta['item']
        image_guid = request.url.split('/')[-1][:-4]
        return 'full/{0}/{1}.jpg'.format(item['file_paths'], image_guid)
