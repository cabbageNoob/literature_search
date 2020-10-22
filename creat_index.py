'''
Descripttion: 
Author: cjh (492795090@qq.com)
Date: 2020-10-17 16:00:39
'''
import pymysql, time

from elasticsearch import Elasticsearch, helpers
es = Elasticsearch()
print(es.ping())

def set_mapping():
    body = {
        "mappings": {
            "doc": {
                "properties": {
                    "title": {
                        "type": "text"
                    },
                    "author": {
                        "type":"text"
                    },
                    "abstract": {
                        "type":"text"
                    },
                    "keywords": {
                        "type":"text" 
                    },
                    "url": {
                        "type":"keyword" 
                    }
                }
            }
        }
    }
    print(es.indices.create(index='paper',body=body))
    # print(es.index(index='p1', doc_type='doc', id=1, body={"name":"lou"}))

def set_datas():
    db = pymysql.connect("localhost", "root", "", "paper", charset='utf8')
    cursor = db.cursor()
    # SQL查询语句
    sql = """
            select * from arxiv
        """
    try:
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
    except Exception as identifier:
        print(identifier)
        db.rollback()
    action = (
        {
            "_index": "paper",
            "_type": "doc",
            "_source": {
                "title": i[0],
                "url":i[1],
                "author": i[2],
                "keywords": i[3],
                "abstract": i[4]
            }
        } for i in result)
    # print(action,next(action))
    t1 = time.time()
    helpers.bulk(es, action)
    print(time.time()-t1)
    return result

if __name__ == '__main__':
    # set_mapping()
    set_datas()
    # print(es.indices.get_mapping(index='paper'))