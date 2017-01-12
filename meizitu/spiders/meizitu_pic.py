# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from meizitu.items import MeizituItem
import string


class Meizispider(scrapy.Spider):
    name = 'meizitu'
    allowed_domains=['mzitu.com']
    start_urls=['http://www.mzitu.com/all']

    def parse(self, response):#爬去主页面的所有连接
        item=MeizituItem()
        content=response.xpath('//ul[@class="archives"]/li/p[2]/a')
        for single in content:
            item['file_name']=single.re('target="_blank">(.*?)</a>')[0]
            page_url=single.xpath('@href').extract()
            # yield item
            yield Request(url=page_url,callback=self.get_all_page,meta={'page_url':page_url})
    def get_all_page(self,response):#爬去所有页面的链接
        # print(response.text)
        page_url=response.meta['page_url']
        max_span=response.xpath('//div[@class="pagenavi"]/a/span/text()').extract()[-2]
        for page in range(1,int(max_span)+1):
            singe_page_url = page_url+'/'+str(page)
            yield Request(url=singe_page_url,callback=self.get_all_picture)
    def get_all_picture(self,resposne):#爬去所有页面图片地址链接
        item = MeizituItem()
        image_url=resposne.xpath('//div[@class="main-image"]/p/a/img/@src').extract()
        image_name=image_url[-9:-4]
        item['image_url']=image_url
        item['image_name']=image_name+'.jpg'
        print(item)
        # yield item
        yield Request(url=image_url,callback=self.download,meta={'image_name':image_name})
    def download(self,response):
        item = MeizituItem()
        # print('照片··',response.content)
        item['image_content']= response
        item['image_name'] = response.meta['image_name'] + '.jpg'
        yield item

