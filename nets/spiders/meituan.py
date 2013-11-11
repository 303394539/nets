import sys,os
sys.path.append(os.path.abspath('./bin/'))

import DB as db

from scrapy.spider import BaseSpider
from scrapy.selector import XmlXPathSelector

class CitySpider(BaseSpider):
    name = 'meituan.city'
    allowed_domains = ['meituan.com']
    start_urls = ['http://www.meituan.com/api/v1/divisions']

    def parse(self,response):
        xxs = XmlXPathSelector(response)
        citys = xxs.select('//division')
        list = []
        for city in citys:
            list.append((
                    city.select('id/text()').extract()[0],
                    city.select('name/text()').extract()[0],
                    city.select('location/latitude/text()').extract()[0],
                    city.select('location/latitude/text()').extract()[0]
                ))
        sql = 'insert into city_meituan (m_id,`name`,latitude,longtitude)value(%s,%s,%s,%s)'
        trun = 'truncate table city_meituan'
        db.batchSQL(sql=sql,list=list,trun=trun)

class GoodsSpider(BaseSpider):
    name = 'meituan.goods'
    allowed_domains = ['meituan.com']
    start_urls = ['http://www.meituan.com/api/v2/beijing/deals']

    def parse(self,response):
        xxs = XmlXPathSelector(response)
        goods = xxs.select('//deals')
        print goods[0]
