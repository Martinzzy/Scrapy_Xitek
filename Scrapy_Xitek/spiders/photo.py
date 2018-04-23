# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from ..items import XitekItem,XitekItemLoader


class PhotoSpider(scrapy.Spider):
    name = 'photo'
    allowed_domains = ['photo.xitek.com']
    start_urls = ['http://photo.xitek.com/']

    custom_settings = {
        'COOKIES_ENABLED':False,
        'DOWNLOAD_DELAY':3,
        'DEFAULT_REQUEST_HEADERS':{
            'Accept':'text/html,application/ xhtml + xm…plication / xml;q = 0.9, */*;q = 0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN, zh;q =0.8,zh-TW;q =0.7, zh-HK;q =0.5, en-US;q =0.3,en;q =0.2',
            'Cache - Control':'no-cache',
            'Connection':'keep-alive',
            'Upgrade-Insecure-Requests':'1',
            'Referer': 'http://photo.xitek.com/',
            'Cookie':'rb6q_2ce7_lastvisit=1524466196; rb6q_2ce7_sid=lh0ZRe; rb6q_2ce7_lastact=1524469861%09member.php%09logging; __utma=233478537.256474385.1524469800.1524469800.1524469800.1; __utmb=233478537.15.10.1524469800; __utmc=233478537; __utmz=233478537.1524469800.1.1.utmcsr=photo.xitek.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utmt_~1=1; __utmt_~2=1; rb6q_2ce7_curname=lyh_zzy; rb6q_2ce7_auth=941ck6%2Fs7g3jkqC5jr8zZinyCZerKTdqZlh9o%2BXboFGO0h5%2FiP2EMIQ0uNZDFieNlBbRkm7r%2BZkfv6C1dVikouxmgf1J; bbuserid=9725512; bbuserid2=9725512; bbpassword=ae911d3f2573547ac1bfd609f68acb6a; votename=lyh_zzy; photobook=K0wqALzi33WFavgFUFhWJJ4mt76pqn6X; rb6q_2ce7__refer=%252Fhome.php%253Fmod%253Dspacecp%2526ac%253Dpm%2526op%253Dchecknewpm%2526rand%253D1524469849; rb6q_2ce7_sendmail=1; Hm_lvt_dd00b3895ef99d3494e3cb06e718ef98=1524469853; Hm_lpvt_dd00b3895ef99d3494e3cb06e718ef98=1524469853',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
        }
    }

    def parse(self, response):
        pattern = r'/photoid/\d{1,6}'
        le = LinkExtractor(allow=pattern)
        links = le.extract_links(response)
        image_url = response.css("div#container .element a img::attr(src)").extract()
        image_url = [x for x in image_url if x.endswith('thumb.jpg')]
        for link in links:
            detail_url = link.url
            yield Request(url=detail_url,callback=self.parse_image,dont_filter=True,meta={"image_urls":image_url})

        #下一页的url
        next_url = response.css('.bnext::attr(href)').extract_first()
        if next_url:
            url = response.urljoin(next_url)
            yield Request(url=url,callback=self.parse,dont_filter=True)

    #解析每张图片的具体数据信息
    def parse_image(self,response):
        item_loader = XitekItemLoader(item=XitekItem(),response=response)
        url = response.url
        pattern = r'http://photo.xitek.com/photoid/(\d+)'
        photo_id = int(re.findall(pattern,url)[0])
        image_url = response.meta.get("image_urls","")
        item_loader.add_value("id",photo_id)
        item_loader.add_css("author",".author a::text")
        item_loader.add_css("title","div.group_img_title::text")
        item_loader.add_value("image",[image_url])
        item_loader.add_css("time",".group_img_title span.date::text")
        item_loader.add_css("view_num",".views::text")
        item_loader.add_css("comment_num",".replys::text")
        item_loader.add_css("favorite_num",".good::text")
        item_loader.add_value("crawl_time",datetime.datetime.now())
        photo = item_loader.load_item()
        yield photo