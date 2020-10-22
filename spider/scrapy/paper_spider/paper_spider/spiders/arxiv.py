'''
Descripttion: 
Author: cjh (492795090@qq.com)
Date: 2020-10-16 09:26:20
'''
# -*- coding: utf-8 -*-
import scrapy
import urllib


class ArxivSpider(scrapy.Spider):
    name = 'arxiv'
    allowed_domains = ['arxiv.org']
    start_urls = ['https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=&terms-0-field=title&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first&start=0']

    def parse(self, response):
        next_url=response.xpath('//div[@class="content"]/nav/a[@class="pagination-next"]/@href').extract_first()
        next_url = urllib.parse.urljoin(response.url, next_url)
        yield scrapy.Request(
            next_url,
            callback=self.parse
            )
            
        papers = response.xpath('//div[@class="content"]/ol[@class="breathe-horizontal"]/li[@class="arxiv-result"]')
        for paper in papers:
            item = {}
            item['title'] = paper.xpath('./p[@class="title is-5 mathjax"]/text()').extract_first().strip()
            item['author'] = paper.xpath('./p[@class="authors"]/a/text()').extract()
            # item['keywords'] = paper.xpath('./')
            item['pdf_href'] = paper.xpath('./div[@class="is-marginless"]/p/span/a[text()="pdf"]/@href').extract_first()
            item['abstract'] = paper.xpath('./p[@class="abstract mathjax"]/span[@class="abstract-short has-text-grey-dark mathjax"]/text()').extract_first().strip()
            yield item