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
            "bool": {
                "should": [
                    {
                        "match": {
                            "title":msg
                        }
                    },
                    # {
                    #     "match": {
                    #         "abstract":msg
                    #     }
                    # }
                ]
            }
        },
        "highlight": {
            "pre_tags": "<b style='color:red;font-size:20px;>",
            "post_tags": "</b>",
            "fields": {
                "title": {},
                # "abstract": {}
            }
        }
    }
    res = es.search(index='paper', body=body)
    # print(json.dumps((res['hits']), indent=4, ensure_ascii=False))
    return res['hits']

if __name__ == '__main__':
    filter_msg('correct')