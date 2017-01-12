# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from meizitu.items import MeizituItem
import re
import os
import requests

class MeizituPipeline(object):
    def process_item(self, item, spider):
        # isExists=os.path.join('D:\学习\GitHub\meizitu\meizitu',item['file_name'])
        #
        # if not isExists:
        #     print(u'开始创建一个名字为'+item['file_name']+'文件夹')
        #     os.makedirs(os.path.join('D:\学习\GitHub\meizitu\meizitu',item['file_name']))
        # else:
        #     print(u'名字叫', item['file_name'], u'的文件夹已经存在了')
        # os.chdir('D:\\学习\\GitHub\\meizitu\\meizitu\\'+item['file_name'])
        with open(item['img_name'].jpg,'ab') as img:
            img.write()
