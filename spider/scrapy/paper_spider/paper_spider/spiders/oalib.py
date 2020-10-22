'''
Descripttion: 
Author: cjh (492795090@qq.com)
Date: 2020-10-12 09:10:59
'''
# -*- coding: utf-8 -*-
import scrapy
import urllib
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class OalibSpider(CrawlSpider):
    name = 'oalib'
    allowed_domains = ['oalib.com','scielo.br','dx.doi.org','ispacs.com']
    start_urls = ['https://www.oalib.com/lib/showJournalListOfPublishing']# ,'https://www.oalib.com/lib/showJournalList',''

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="paperlist"]'), callback='parse_item'),
    )

    def parse_item(self, response):
        ul_list = response.xpath('//div[@class="paperlist"]/ul')
        for ul in ul_list:
            li_list = ul.xpath('./li')
            for li in li_list:
                href = li.xpath('.//a/@href').extract_first()
                href = urllib.parse.urljoin(response.url, href)
                yield scrapy.Request(
                    href,
                    callback=self.parse_publish
                )


    def parse_publish(self, response):
        paper_list = response.xpath('//div[@class="paperlist"]')
        for paper in paper_list:
            paper_href = paper.xpath('./h4/a/@href').extract_first()
            paper_href = urllib.parse.urljoin(response.url, paper_href)
            yield scrapy.Request(
                paper_href,
                callback=self.parse_paper_detail
            )

        pageinfo =  re.findall('//www.oalib.com\',\d+,\d+,\d+,\d+', response.body.decode())[0]
        page_count = int(pageinfo.split(',')[2])
        current_page = int(pageinfo.split(',')[3])
        if current_page < page_count:
            yield scrapy.Request(
                '/'.join(response.url.split('/')[:-1])+'/'+str(current_page+1),
                callback=self.parse_publish
            )
            

    def parse_paper_detail(self, response):
        item = {}
        paper_content = response.xpath('//div[@class="contents"]')
        item['title'] = paper_content.xpath('./h1/text()').extract_first()
        item['doi'] = paper_content.xpath('./p[@class="doi"]/a/@href').extract_first()
        next_url = item['doi']
        if next_url is None:
            next_url = paper_content.xpath('.//p[@class="resetHref"]/a/@href')[0]
        item['author'] = paper_content.xpath('./div[@class="authors"]/a/text()').extract()
        item['keywords'] = paper_content.xpath('./p[@class="keyword"]/a/text()').extract()
        item['abstract'] = paper_content.xpath('./span//p/text()').extract_first()
        yield scrapy.Request(
            next_url,
            callback=self.parse_pdf_href,
            meta={'item': item}
        )
        

    def parse_pdf_href(self, response):
        item = response.meta['item']
        pdf_href = response.xpath('//div[@class="box"]/ul/li/a[contains(text(), "English (pdf)")]/@href').extract_first()
        pdf_href = urllib.parse.urljoin(response.url, pdf_href)
        item['pdf_href'] = pdf_href
        yield item
        # print(item)
