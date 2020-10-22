'''
Descripttion: 
Author: cjh (492795090@qq.com)
Date: 2020-10-11 21:56:02
'''
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

db = pymysql.connect("localhost", "root", "", "paper", charset='utf8')
cursor = db.cursor()

class PaperSpiderPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'ICLR':
            with open('./paper_ICLR.txt', 'a+', encoding='utf8') as f:
                f.write(item['title'] + '\t' + item['pdf_href'] + '\n')
        elif spider.name == 'PMLR':
            sql = """
                insert into pmlr(title, url, author, abstract)\
                value(%s, %s, %s, %s)
            """
            try:
                cursor.execute(sql, (item['title'], item['pdf_href'], str(item['author']), item['abstract']))
                db.commit()
            except Exception as identifier:
                print(identifier)
                db.rollback()
        elif spider.name == 'oalib':
            # with open('./paper_oalib.txt', 'a+', encoding='utf8') as f:
            #     f.write(item['title'] + '\t' + item['pdf_href'] + '\n')
            # SQL插入语句
            sql = """
                insert into oalib(title, url, author, keywords, abstract)\
                value(%s, %s, %s, %s, %s)
            """
            try:
                cursor.execute(sql, (item['title'], item['pdf_href'], str(item['author']), str(item['keywords']), item['abstract']))
                db.commit()
            except Exception as identifier:
                print(identifier)
                db.rollback()
        elif spider.name == 'arxiv':
            sql = """
                insert into arxiv(title, url, author, abstract)\
                value(%s, %s, %s, %s)
            """
            try:
                cursor.execute(sql, (item['title'], item['pdf_href'], str(item['author']), item['abstract']))
                db.commit()
            except Exception as identifier:
                print(identifier)
                db.rollback()
        return item

class OalibSpiderPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'oalib':
            # with open('./paper_oalib.txt', 'a+', encoding='utf8') as f:
            #     f.write(item['title'] + '\t' + item['pdf_href'] + '\n')
            # SQL插入语句
            sql = """
                insert into oalib(title, url, author, keywords, abstract)\
                value(%s, %s, %s, %s, %s)
            """
            print(item)
            try:
                cursor.execute(sql, (item['title'], item['pdf_href'], str(item['author']), str(item['keywords']), item['abstract']))
                db.commit()
            except Exception as identifier:
                print(identifier)
                db.rollback()
        return item

# if __name__ == '__main__':
#     sql = """
#                 insert into oalib(title, url, author, keywords, abstract)\
#                 value(%s, %s, %s, %s, %s)
#             """
#     try:
#         cursor.execute(sql, ('z', 's', 'e', 't', 'y'))
#         db.commit()
#     except Expression as identifier:
#         db.rollback()


