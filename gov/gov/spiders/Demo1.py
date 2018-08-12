# -*- coding: utf-8 -*-
import scrapy
import json 
from scrapy import Request 
import re
from gov.items import ComposerItem,CommentItem
import datetime
class Demo1Spider(scrapy.Spider):
    name = 'Demo1'
    allowed_domains = ['http://www.tjgp.gov.cn/']
    start_urls = ['http://www.tjgp.gov.cn/portal/topicView.do?method=view&view=Infor&id=1665&ver=2&st=1']
    def parse(self, response):
        post_url = 'http://www.tjgp.gov.cn/portal/topicView.do%s'
        # 先取出所有的节点
        post_list = response.xpath('//*[@id="leftColumn"]/div/ul[2]/li[2]/div/a')
        for post in post_list:
            pid = post.xpath('./@href').get()
            url = post_url % pid
            pages = post.xpath('./span/text()').extract_first()
            request = Request(url + pid,callback=self.parse_post,dont_filter=True)
            request.meta['title']= post.xpath('./text()').extract_first()
            request.meta['url'] = url 
            request.meta['pages'] = re.sub("[^\d]+","",pages).strip(' ')
            yield request 
        other_pages = response.xpath('//*[@id="leftColumn"]/div/ul/a/@href').extract()
        yield from[response.follow(page) for page in other_pages]
    def parse_post(self,response):
        post = ComposerItem()
        # 公告标题
        post['title'] = response.meta['title']
        # 公告网页
        post['url'] = response.meta['url']
        # 公告页数    
        post['pages'] = response.meta['pages']
        # 获取当前时间
        post['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        yield post
        page_url = 'http://www.tjgp.gov.cn/portal/topicView.do'
        for clip in [1664,1665]:
            for number in range(1,2000):
                json_comper = {"method":"view",
                        "page":str(number),
                        "id":str(clip),
                        "step":"1",
                        "view":"Infor",
                        "ldateQGE":"",
                        "ldateQLE":""}
                yield scrapy.FormRequest(
                    url = page_url,
                    formdata = json_comper,
                    callback = self.parse_comment,dont_filter=True
                )
    def parse_comment(self,response):
        reflshPages = response.xpath('//*[@id="reflshPage"]/ul/li')
        for reflshPage in reflshPages:
            # 存到json和csv文件里面,注释掉37行yield post
            # item = CommentItem()
            # 公告正文
            # item['content'] = reflshPage.xpath('./a/text()').extract_first()
            # 发布时间
            # item['public_time'] = reflshPage.xpath('./span/text()').extract_first()
            # 公告链接
            # item['content_url'] = reflshPage.xpath('./a/@href').extract_first()
            # yield item   
             
            comment = CommentItem()
            #公告正文
            comment['content'] = reflshPage.xpath('./a/text()').extract_first()
            #发布时间
            comment['public_time'] = reflshPage.xpath('./span/text()').extract_first()
            #公告链接
            comment['content_url'] = reflshPage.xpath('./a/@href').extract_first()
            yield comment