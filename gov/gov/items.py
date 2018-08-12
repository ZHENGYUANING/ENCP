# -*- coding: utf-8 -*-
# Define here the models for your scraped items
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy import Field
class ComposerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name = 'composers'
    title = Field()
    url = Field()
    pages = Field()
    create_time = Field()
class CommentItem(scrapy.Item):
    table_name = 'comments'
    content = Field()
    public_time = Field()
    content_url = Field()