#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/10/12 15:30
# @Author : LWK
# @Email   : 1293532247@qq.com
# @File : spider_main.py
# @Software: PyCharm

from spider_paper import config
from spider_paper import spider_store
from bs4 import BeautifulSoup
import requests
import re
import time
import threading
import os

'''
链接分5级
level 0: 官网 http://www.oalib.com/
level 1: 出版社 http://www.oalib.com/lib/showJournalListOfPublishing
level 2: 期刊 http://www.oalib.com/lib/showJournalListModle?filter=AGH%20University%20of%20Science%20and%20Technology%20Press
level 3: 论文列表 http://www.oalib.com/journal/4054/1#.X4eyqdAzZdg
level 4: 论文页 http://www.oalib.com/paper/2921356#.X4eyvdAzZdg
'''

url_total = 'http://www.oalib.com/lib/showJournalListOfPublishing'


# 清理字符串
def str_clean(strs):
    return strs.strip().replace('\r', '').replace('\n', '').replace('\t', '')


# 获取期刊链接（2级），输入为1级链接，返回一个列表
def spider_pagelist(url):
    try:
        r = requests.get(url, headers=config.headers, proxies=config.proxies, timeout=10)
        # r = requests.get(url, headers=config.headers, timeout=10)
        r.raise_for_status()
        # r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        main_page = soup.find_all('div', class_='paperlist')
        # paperlinks = []
        pagelinks = []
        # main_page = soup.find_all('tr')
        alphas = main_page[0].find_all('ul')
        for alpha in alphas:
            papers = alpha.find_all('li')
            for paper in papers:
                pagelinks.append((str_clean(paper.h3.a.string), config.url_head + paper.h3.a['href'][2:]))
        return pagelinks
    except:
        return "产生异常"


# 获取列表页链接（3级），输入为2级链接，返回一个列表
def spider_pagelist_2(url):
    try:
        r = requests.get(url, headers=config.headers, proxies=config.proxies, timeout=10)
        # r = requests.get(url, headers=config.headers, timeout=10)
        r.raise_for_status()
        # r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        main_page = soup.find_all('div', class_='paperlist')
        # paperlinks = []
        pagelinks = []
        # main_page = soup.find_all('tr')
        alphas = main_page[0].find_all('ul')
        for alpha in alphas:
            papers = alpha.find_all('li')
            for paper in papers:
                pagelinks.append((str_clean(paper.h4.a.string), config.url_head + paper.h4.a['href'][2:]))
        return pagelinks
    except:
        return "产生异常"


# 获取页面数量，输入为3级链接，返回页面数量和当前页论文数量
def spider_count(url):
    try:
        r = requests.get(url, headers=config.headers, proxies=config.proxies, timeout=30)
        # r = requests.get(url, headers=config.headers, timeout=30)
        r.raise_for_status()
        # r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        ulist = []
        main_page = r.text
        ls = re.findall('//www.oalib.com\',\d+,\d+,\d+,\d+', main_page)[0].split(',')
        pagecount = eval(ls[2])
        papercount = eval(ls[-1])
        return pagecount, papercount
    except:
        return '产生异常', '产生异常'


# 获取页面中论文的内容链接（4级），输入为3级链接，返回一个列表
def spider_paperlist(url):
    try:
        r = requests.get(url, headers=config.headers, proxies=config.proxies, timeout=30)
        # r = requests.get(url, headers=config.headers, timeout=30)
        r.raise_for_status()
        # r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        ulist = []
        paperlist = soup.find_all('div', class_='paperlist')
        for paper in paperlist:
            ulist.append((paper.h4.a.span.string, config.url_head + paper.h4.a['href'][2:]))
        # print(len(main_page))
        return ulist
    except:
        return '产生异常'


# 获取论文的关键词，输入为4级链接，返回关键词列表
def spider_paper_messages(url):
    try:
        r = requests.get(url, headers=config.headers, proxies=config.proxies, timeout=30)
        # r = requests.get(url, headers=config.headers, timeout=30)
        r.raise_for_status()
        # r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        key_page = soup.find_all('p', class_='keyword')
        author_page = soup.find_all('div', class_='authors')
        doi_page = soup.find_all('p', class_='doi')
        doi = ''
        keywords = []
        authors = []
        if len(key_page) > 0:
            for key in key_page[0].find_all('a'):
                if str(key.string) != 'None':
                    keywords.append(str_clean(key.string))
        if len(author_page) > 0:
            for author in author_page[0].find_all('a'):
                if str(author.string) != 'None':
                    authors.append(str_clean(author.string))
        if len(doi_page) == 1:
            doi = doi_page[0].a.u.string
        return keywords, authors, doi
    except:
        return '产生异常', '产生异常', '产生异常'


def spider_test(url):
    try:
        r = requests.get(url, headers=config.headers, proxies=config.proxies, timeout=30)
        # r = requests.get(url, headers=config.headers, timeout=30)
        r.raise_for_status()
        # r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        paperlist = soup.find_all('div', class_='paperlist')
        papers = paperlist.findall('ul')
        linklist = []
        for paper in papers:
            paperlink = paper.findall('li')
            for link in paperlink:
                linklist.append(link.h3.a['href'])
        # print(len(linklist))
    except:
        return "产生异常"


def spider_main(url_one):
    # url_zero = 'http://www.oalib.com/'
    # url_one = 'http://www.oalib.com/lib/showJournalListOfPublishing'
    # print('********** 1 ************')
    url_twos = spider_pagelist(url_one)  # 由一级链接得到二级链接
    if url_twos == '产生异常':
        # spider_main(url_one)
        return 'error'
    # print('********** 2 *************')
    for title_two, url_two in url_twos:
        # print(title_two, ' ', url_two)
        # time.sleep(0.05)
        # print('********** 3 *************')
        url_threes = spider_pagelist_2(url_two)  # 由二级链接得到三级链接
        if url_threes == '产生异常':
            # spider_main(url_one)
            return 'error'
        # print(url_threes)
        # print('********** 4 *************')
        for title_three, url_three in url_threes:
            # time.sleep(0.05)
            filedata = []
            if spider_store.spider_done_page.get(title_three) != None:
                print(title_three + '.json is already exist!')
                continue
            print(title_three, ' ', url_three)
            # print('********** 5 *************')
            pagecount, papercount = spider_count(url_three)  # 由三级链接得到页数和每页论文数
            if pagecount == '产生异常':
                # spider_main(url_one)
                return 'error'
            # print('********** 6 *************')
            print(pagecount, ' ', papercount)
            page_list_head = url_three[:-1]
            for i in range(1, pagecount + 1):
                # time.sleep(0.05)
                # print('********** 7 *************')
                paperlist = spider_paperlist(page_list_head + str(i))  # 由三级链接得到论文列表
                if paperlist == '产生异常':
                    # spider_main(url_one)
                    return 'error'
                # print(paperlist)
                # print('********** 8 *************')
                for title_paper, paper in paperlist:
                    time.sleep(spider_store.time_space)
                    # print('********** 9 *************')
                    paper_keywords, paper_authors, paper_doi = spider_paper_messages(paper)  # 由四级链接得到论文信息
                    if paper_keywords == '产生异常':
                        # spider_main(url_one)
                        return 'error'
                    # print('********** 10 *************')
                    paper_dict = {'Name': title_paper, 'Link': paper, 'Keywords': paper_keywords,
                                  'Authors': paper_authors, 'Doi': paper_doi}
                    # spider_store.data.append(paper_dict)
                    filedata.append(paper_dict)
                    # print(len(spider_store.data))
                    # print(paper, ' ', len(filedata), '/', papercount)
                    print(paper + ' ' + str(len(filedata)) + '/' + str(papercount))
            filename = title_three
            spider_store.store(filedata, filename)
            # return filename
            # if len(spider_store.data) == 11:
            #     return 0
            # print(pagecount, ' ', papercount)
    return 'spider success'


if __name__ == '__main__':
    spider_store.read()
    print(spider_store.spider_done_page)
    # while 1:
    spider_result = spider_main(url_total)
    print(spider_result)
    # if spider_result == 'error':
    #     spider_result = spider_main(url_total)
    # else:
    #     break
    # spider_store.store(spider_store.data, filename)
    # a, b, c = spider_paper_messages(url)
    # print(b)
