# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DmozItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class TorrentItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    size = scrapy.Field()

class FuwuPurchaseItem(scrapy.Item):
    buyerNameMasked = scrapy.Field()
    buyerRank = scrapy.Field()
    purchaseTime = scrapy.Field()
    licLength = scrapy.Field()
    licVersion = scrapy.Field()
    fuwuISV = scrapy.Field()
        
class FuwuISVItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()