# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeizituItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_name = scrapy.Field()
    image_url = scrapy.Field()
    # images = scrapy.Field()
    file_paths= scrapy.Field()
