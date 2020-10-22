'''
Descripttion: 
Author: cjh (492795090@qq.com)
Date: 2020-10-11 23:01:01
'''
# -*- coding: utf-8 -*-
import scrapy


class IclrSpider(scrapy.Spider):
    name = 'ICLR'
    allowed_domains = ['iclr.cc']
    start_urls = ["https://iclr.cc/Conferences/2018/Schedule?type=Poster", "https://iclr.cc/Conferences/2018/Schedule?type=Oral"]

    def parse(self, response):
        for poster in response.xpath('//div[starts-with(@id, "maincard_")]'):
            # item = PapercrawlerItem()
            item={}
            item["title"] = poster.xpath('.//div[@class="maincardBody"]/text()[1]').get()
            item["pdf_href"] = poster.xpath('.//a[@title="PDF"]/@href').get()
            yield item
