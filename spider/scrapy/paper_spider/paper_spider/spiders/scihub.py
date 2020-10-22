'''
Descripttion: 
Author: cjh (492795090@qq.com)
Date: 2020-10-18 22:36:46
'''
# -*- coding: utf-8 -*-
import scrapy
import urllib

class ScihubSpider(scrapy.Spider):
    name = 'scihub'
    allowed_domains = ['booksc.org']
    start_urls = ['https://booksc.org/journals/A']

    def parse(self, response):
        tr_lists = response.xpath('//table[@class="table table-striped table-hover journals-table"]/tbody/tr')
        for tr in tr_lists:
            publish_url = tr.xpath('./td/a/@href').extract_first()
            publish_url = 'https://booksc.org' + publish_url
            yield scrapy.Request(
                publish_url,
                callback=self.parse_publisher,
                dont_filter=True
            )

        # 分页
        next_page_url = response.xpath('//a[text()="Next page »"]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(
                next_page_url,
                callback=self.parse
            )
        # 分类
        


    def parse_publisher(self, response):
        years = response.xpath('//div[@class="table"]/div[@class="row"]')[1:]
        for year in years:
            a_list = year.xpath('.//div[@class="item col-sm-1"]/a/@href').extract()
            for a in a_list:
                article_list_url = 'https://booksc.org' + a
                yield scrapy.Request(
                    article_list_url,
                    callback=self.parse_article_list
                )

    def parse_article_list(self, response):
        article_list=response.xpath('//div[@id="searchResultBox"]/div[@class="resItemBox resItemBoxArticles exactMatch"]')
        for article in article_list:
            next_url = article.xpath('.//h3/a/@href').extract_first()
            yield scrapy.Request(
                urllib.parse.urljoin(response.url, next_url),
                callback=self.parse_article,
            )

    def parse_article(self,response):
        item = {}
        content = response.xpath('//div[@class="col-sm-9"]')
        item['title'] = content.xpath('./h1/text()').extract_first().strip()
        item['author'] = content.xpath('./i/a/text()').extract()
        item['publish_data'] = content.xpath('.//div[@class="bookDetailsBox"]/div[@class="bookProperty property__date"]/div[@class="property_value"]/text()').extract_first()
        # item['pdf_href'] = response.xpath('//a[@class="btn btn-primary dlButton addDownloadedBook"]/@href').extract_first()
        # item['pdf_href'] = urllib.parse.urljoin(response.url, item['pdf_href'])
        item['pdf_href'] = response.url
        yield item

 