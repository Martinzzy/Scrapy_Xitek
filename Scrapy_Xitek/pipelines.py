# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi

class ScrapyXitekPipeline(object):
    def process_item(self, item, spider):
        return item

#twisted只是提供一个容器，进行异步存储
class MySQLTwistedPipeline(object):

    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
                host = settings['MYSQL_HOST'],
                db = settings['MYSQL_DBNAME'],
                user = settings['MYSQL_USER'],
                passwd = settings['MYSQL_PASSWORD'],
                port = settings['MYSQL_PORT'],
                charset = 'utf8',
                cursorclass = pymysql.cursors.DictCursor,
                use_unicode = True,
            )

        dbpool = adbapi.ConnectionPool("pymysql",**dbparms)
        return cls(dbpool)


    def process_item(self,item,spider):
        #使用twisted使mysql的插入编程异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)


    def handle_error(self,failure):
        #处理异步插入的异常
        print(failure)

    def do_insert(self,cursor,item):
        #执行具体的插入
        #使用item中定义的函数
        insert_sql,params = item.get_insert_sql()
        cursor.execute(insert_sql,params)