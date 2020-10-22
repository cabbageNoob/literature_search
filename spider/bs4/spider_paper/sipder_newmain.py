#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/18 20:02
# @Author  : lwk
# @Email   : 1293532247@qq.com
# @File    : sipder_newmain.py
# @Software: PyCharm

from spider_paper import config
from spider_paper import spider_store
from bs4 import BeautifulSoup
import requests
import re
import time
import threading
import random

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


class mythread(threading.Thread):
    def __init__(self, threadID, name, url, title_paper, dataset, papercount):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.url = url
        self.dataset = dataset
        self.title_paper = title_paper
        self.papercount = papercount

    def run(self):
        print("开启线程： " + self.name)
        paper_keywords, paper_authors, paper_doi, paper_abstract = spider_paper_messages(self.url)
        # print(paper_keywords, paper_authors, paper_doi)
        paper_dict = {'Name': self.title_paper, 'Link': self.url, 'Keywords': paper_keywords,
                      'Authors': paper_authors, 'Doi': paper_doi, 'Abstract': paper_abstract}
        print(paper_dict)
        self.dataset.append(paper_dict)
        # + '/' + str(papercount))
        print(self.url + ' ' + str(len(self.dataset)) + '/' + str(self.papercount))


# 获取期刊链接（2级），输入为1级链接，返回一个列表
def spider_pagelist(url):
    # r = requests.get(url, headers=config.headers, proxies=config.proxies, timeout=10)
    r = requests.get(url, headers=config.headers, timeout=30)
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


# 获取列表页链接（3级），输入为2级链接，返回一个列表
def spider_pagelist_2(url):
    # r = requests.get(url, headers=config.headers, proxies=config.proxies, timeout=10)
    r = requests.get(url, headers=config.headers, timeout=30)
    soup = BeautifulSoup(r.text, 'html.parser')
    main_page = soup.find_all('div', class_='paperlist')
    pagelinks = []
    alphas = main_page[0].find_all('ul')
    for alpha in alphas:
        papers = alpha.find_all('li')
        for paper in papers:
            pagelinks.append((str_clean(paper.h4.a.string), config.url_head + paper.h4.a['href'][2:]))
    return pagelinks


# 获取页面数量，输入为3级链接，返回页面数量和当前页论文数量
def spider_count(url):
    # r = requests.get(url, headers=config.headers, proxies=config.proxies, timeout=30)
    r = requests.get(url, headers=config.headers, timeout=30)
    soup = BeautifulSoup(r.text, 'html.parser')
    ulist = []
    main_page = r.text
    ls = re.findall('//www.oalib.com\',\d+,\d+,\d+,\d+', main_page)[0].split(',')
    pagecount = eval(ls[2])
    papercount = eval(ls[-1])
    return pagecount, papercount


# 获取页面中论文的内容链接（4级），输入为3级链接，返回一个列表
def spider_paperlist(url):
    # r = requests.get(url, headers=config.headers, proxies=config.proxies, timeout=30)
    r = requests.get(url, headers=config.headers, timeout=30)
    soup = BeautifulSoup(r.text, 'html.parser')
    ulist = []
    paperlist = soup.find_all('div', class_='paperlist')
    for paper in paperlist:
        ulist.append((paper.h4.a.span.string, config.url_head + paper.h4.a['href'][2:]))
    # print(len(main_page))
    return ulist


# 获取论文的关键词，输入为4级链接，返回关键词列表
def spider_paper_messages(url):
    # r = requests.get(url, headers=config.headers, proxies=config.proxies, timeout=30)
    r = requests.get(url, headers=config.headers, timeout=30)
    soup = BeautifulSoup(r.text, 'html.parser')
    key_page = soup.find_all('p', class_='keyword')
    author_page = soup.find_all('div', class_='authors')
    doi_page = soup.find_all('p', class_='doi')
    content_page = soup.find('div', class_='contents').children
    abstract = ''
    # print(content_page)
    for content in content_page:
        # print(content.name)
        if content.name == 'span':
            abstract = content.div.p.string
    # abstract_page = content_page.span
    # abstract = content_page.span.div.p.string
    doi = ''
    keywords = []
    authors = []
    # print(len(key_page), len(author_page), len(doi_page))
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
    return keywords, authors, doi, abstract


def spider_test(url):
    # r = requests.get(url, headers=config.headers, proxies=config.proxies, timeout=30)
    r = requests.get(url, headers=config.headers, timeout=30)
    soup = BeautifulSoup(r.text, 'html.parser')
    paperlist = soup.find_all('div', class_='paperlist')
    papers = paperlist.findall('ul')
    linklist = []
    for paper in papers:
        paperlink = paper.findall('li')
        for link in paperlink:
            linklist.append(link.h3.a['href'])
    # print(len(linklist))


def spider_main(url_one):
    url_twos = spider_pagelist(url_one)  # 由一级链接得到二级链接
    for title_two, url_two in url_twos:
        url_threes = spider_pagelist_2(url_two)  # 由二级链接得到三级链接
        for title_three, url_three in url_threes:
            filedata = []
            if spider_store.spider_done_page.get(title_three) != None:
                print(title_three + '.json is already exist!')
                continue
            print(title_three, ' ', url_three)
            pagecount, papercount = spider_count(url_three)  # 由三级链接得到页数和每页论文数
            print(pagecount, ' ', papercount)
            page_list_head = url_three[:-1]
            for i in range(1, pagecount + 1):
                threads = []
                count = 1
                paperlist = spider_paperlist(page_list_head + str(i))  # 由三级链接得到论文列表
                for title_paper, paper in paperlist:
                    # time.sleep(spider_store.time_space)
                    newthread = mythread(count, 'Thread ' + str(count), paper, title_paper, filedata, papercount)
                    count += 1
                    time.sleep(random.random())
                    newthread.start()
                    threads.append(newthread)
                    # paper_keywords, paper_authors, paper_doi = spider_paper_messages(paper)  # 由四级链接得到论文信息
                    # paper_dict = {'Name': title_paper, 'Link': paper, 'Keywords': paper_keywords,
                    #               'Authors': paper_authors, 'Doi': paper_doi}
                    # filedata.append(paper_dict)
                    # print(paper + ' ' + str(len(filedata)) + '/' + str(papercount))
                for t in threads:
                    # time.sleep(0.15)
                    t.join()
            filename = title_three
            # print(filedata)
            spider_store.store(filedata, filename)
    return 'spider success'


def spider_journal(url_two):
    url_threes = spider_pagelist_2(url_two)[2000:]  # 由二级链接得到三级链接
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
        # print('********** 6 *************')
        print(pagecount, ' ', papercount)
        page_list_head = url_three[:-1]
        for i in range(1, pagecount + 1):
            # time.sleep(0.05)
            # print('********** 7 *************')
            paperlist = spider_paperlist(page_list_head + str(i))  # 由三级链接得到论文列表
            # print('********** 8 *************')
            for title_paper, paper in paperlist:
                time.sleep(spider_store.time_space)
                # print('********** 9 *************')
                paper_keywords, paper_authors, paper_doi = spider_paper_messages(paper)  # 由四级链接得到论文信息
                paper_dict = {'Name': title_paper, 'Link': paper, 'Keywords': paper_keywords,
                              'Authors': paper_authors, 'Doi': paper_doi}
                filedata.append(paper_dict)
                print(paper + ' ' + str(len(filedata)) + '/' + str(papercount))
        filename = title_three
        spider_store.store(filedata, filename)


if __name__ == '__main__':
    spider_store.read()
    print(spider_store.spider_done_page)
    # print(len(spider_pagelist(url_total)))
    while True:
        try:
            spider_result = spider_main(url_total)
            if spider_result == 'spider success':
                break
        except:
            continue
    number_1021 = 374
    # url_test = 'http://www.oalib.com/paper/2645956'
    # print(spider_paper_messages(url_test))
    # while 1:
    # spider_result = spider_main(url_total)
    # if spider_result == 'error':
    #     spider_result = spider_main(url_total)
    # else:
    #     break
    # spider_store.store(spider_store.data, filename)
    # a, b, c = spider_paper_messages(url)
    # print(b)
