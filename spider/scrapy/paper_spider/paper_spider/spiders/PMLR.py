'''
Descripttion: 
Author: cjh (492795090@qq.com)
Date: 2020-10-11 21:57:09
'''
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PmlrSpider(CrawlSpider):
    name = 'PMLR'
    allowed_domains = ['proceedings.mlr.press']
    start_urls = ['http://proceedings.mlr.press/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="post-content"]/ul[@class="proceedings-list"]'), callback='parse_item'),
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        papers = response.xpath('//div[@class="paper"]')
        for paper in papers:
            item['title'] = paper.xpath('./p[@class="title"]/text()').extract_first()
            item['pdf_href'] = paper.xpath('./p[@class="links"]/a[text()="Download PDF"]/@href').extract_first()
            item['author'] = paper.xpath('./p[@class="details"]/span[@class="authors"]/text()').extract_first().replace(r'\xa0', '').split(',')
            item['author']=[author.strip() for author in item['author']]
            abs_url = paper.xpath('./p[@class="links"]/a/@href').extract_first()
            yield scrapy.Request(
                abs_url,
                callback=self.get_abs,
                meta={'item':item}
            )

    def get_abs(self, response):
        item = response.meta['item']
        item['abstract'] = response.xpath('//div[@id="abstract"]/text()').extract_first()
        if item['abstract'] is not None:
            item['abstract']=item['abstract'].strip()
        yield item
