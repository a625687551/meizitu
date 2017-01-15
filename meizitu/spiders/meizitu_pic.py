# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from meizitu.items import MeizituItem
import string
import re
from datetime import datetime
import time


class Meizispider(scrapy.Spider):
    name = 'meizitu'
    allowed_domains=['mzitu.com']
    start_urls=['http://www.mzitu.com/all']

    def parse(self, response):#爬去主页面的所有连接
        proxy= response.meta.get('proxy','localhost')
        print(proxy,u'代理开始采集')
        content=response.xpath('//ul[@class="archives"]/li/p[2]/a')
        for single in content:
            page_url=single.xpath('@href').extract()[0]
            yield Request(url=page_url,callback=self.get_all_page,meta={'page_url':page_url})
    def get_all_page(self,response):#爬去所有页面的链接
        page_url=response.meta['page_url']
        max_span=response.xpath('//div[@class="pagenavi"]/a/span/text()').extract()[-2]
        file_paths=response.xpath('//h2[@class="main-title"]/text()').extract()[0].strip()
        print(file_paths)
        for page in range(1,int(max_span)+1):
            singe_page_url = page_url+'/'+str(page)
            yield Request(url=singe_page_url,callback=self.get_all_picture,meta={'file_paths':file_paths})
    def get_all_picture(self,resposne):#爬去所有页面图片地址链接
        item = MeizituItem()
        image_url=resposne.xpath('//div[@class="main-image"]/p/a/img/@src').extract()
        image_name=image_url[0][-9:-4]
        item['file_paths']=resposne.meta['file_paths']
        item['image_url']=image_url
        item['image_name']=re.sub(r'\\/:*?"<>|','',image_name.strip())+'.jpg'
        print(item,datetime.now())
        time.sleep(0.5)
        yield item


