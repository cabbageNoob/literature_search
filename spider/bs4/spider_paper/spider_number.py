#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/18 19:30
# @Author  : lwk
# @Email   : 1293532247@qq.com
# @File    : spider_number.py
# @Software: PyCharm
import json
import os, sys

# 打开文件
# path = "./data/"
path = "./journals/"
dirs = os.listdir(path)
filenames = []
# 输出所有文件和文件夹
for file in dirs:
    # print(file)
    filenames.append(file)

path2 = '../../spider_paper/journals/'
dirs2 = os.listdir(path2)
filenames2 = []
for file in dirs2:
    filenames2.append(file)

number = 0
for file in filenames:
    fp = open(path + file, 'r', encoding='utf-8')
    data = json.load(fp)
    number += len(data)
    fp.close()

for file in filenames2:
    fp = open(path2 + file, 'r', encoding='utf-8')
    data = json.load(fp)
    number += len(data)
    fp.close()

print('Paper count: ', number)
