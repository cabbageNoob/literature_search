#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 14:39
# @Author  : lwk
# @Email   : 1293532247@qq.com
# @File    : spider_test.py
# @Software: PyCharm
from spider_paper import config
from bs4 import BeautifulSoup
import requests

url = 'http://www.oalib.com/paper/890503#.X4fs7tAzZdg'

r = requests.get(url, headers=config.headers, timeout=10)
soup = BeautifulSoup(r.text, 'html.parser')
main_page = soup.find('p', class_='doi')
# print(main_page)
for i in range(1, 2):
    print(i)
