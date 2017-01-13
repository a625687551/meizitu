# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from meizitu.items import MeizituItem
import re
import os
import string
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

class MeizituPipeline(object):
    def process_item(self, item, spider):
        pass

class DownloadImagesPipeline(ImagesPipeline):

    def get_media_requests(self,item,info):#下载图片
        for image_url in item['image_url']:
            yield Request(image_url,meta={'name':item['image_name']})

    def item_completed(self,results,item,info):
        file_paths=[x['path'] for ok,x in results if ok]
        # image_name=request
        # file_paths=item['file_paths']
        if not file_paths:
            raise DropItem(u'图片未下载好{}'.format())
        item['file_paths']=file_paths
        return item
    def file_path(self, request, response=None, info=None):
        item=request.meta['item']



