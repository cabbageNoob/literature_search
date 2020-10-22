#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/10/9 11:25
# @Author : LWK
# @Email   : 1293532247@qq.com
# @File : config.py
# @Software: PyCharm
import scrapy

# v2RayN V3.14
proxies = {'http': 'http://127.0.0.1:10809', 'https': 'https://127.0.0.1:10809'}
kv = {'wd': 'BERT'}
agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36"
headers = {'User-Agent': agent}
url_head = 'http://'
