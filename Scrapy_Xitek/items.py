# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from settings import SQL_DATETIME_FORMAT
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,MapCompose

class ScrapyXitekItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def return_value(value):

    return value

def get_int(value):

    return int(value)


class XitekItemLoader(ItemLoader):

    default_output_processor = TakeFirst()


class XitekItem(scrapy.Item):
    id = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field(output_processor=MapCompose(return_value))
    time = scrapy.Field()
    view_num = scrapy.Field(input_processor=MapCompose(get_int))
    comment_num = scrapy.Field(input_processor=MapCompose(get_int))
    favorite_num = scrapy.Field(input_processor=MapCompose(get_int))
    crawl_time = scrapy.Field()


    def get_insert_sql(self):
        insert_sql = """
            insert into photo (id,author,title,time,view_num,comment_num,favorite_num,crawl_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params = (self["id"],self["author"],self["title"],self["time"],
                  self["view_num"],self["comment_num"],self["favorite_num"],self["crawl_time"].strftime(SQL_DATETIME_FORMAT)
                  )
        return insert_sql,params