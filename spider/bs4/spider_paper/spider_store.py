#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 13:25
# @Author  : LWK
# @Email   : 1293532247@qq.com
# @File    : spider_store.py
# @Software: PyCharm
import json
import re

# data = []
time_space = 0.1
spider_done_page = {}


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


def store(data, path):
    fp = open('journals/' + validateTitle(path) + '.json', 'w', encoding='utf-8')
    json.dump(data, fp, ensure_ascii=False, indent=4)
    fp.close()
    with open('donejournals.txt', 'a', encoding='utf-8') as f:
        f.write(path + '\n')
        f.close()


def read():
    with open('donejournals.txt', 'r', encoding='utf-8') as f:
        for line in f:
            spider_done_page[line.replace('\n', '')] = 1
        f.close()
