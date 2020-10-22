'''
Descripttion: 
Author: cjh (492795090@qq.com)
Date: 2020-10-17 22:07:01
'''
import json
from elasticsearch import Elasticsearch
es = Elasticsearch()

def filter_msg(msg):
    body = {
        "size": 10,
        "query": {
            "match": {
                "title":msg
            }
        }
    }
    res = es.search(index='paper', body=body)
    # print(json.dumps((res['hits']), indent=4, ensure_ascii=False))
    return res['hits']

if __name__ == '__main__':
    filter_msg('correct')