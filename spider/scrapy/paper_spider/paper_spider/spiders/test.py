'''
Descripttion: 
Author: cjh (492795090@qq.com)
Date: 2020-10-15 10:01:12
'''
# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['oalib.com']
    start_urls = ['http://www.oalib.com/paper/2914541']

    def parse(self, response):
        print(response.body.decode())
