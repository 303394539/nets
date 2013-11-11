
from scrapy.spider import BaseSpider
from scrapy.selector import XmlXPathSelector

from nets.items import DianpingItem

class CitySpider(BaseSpider):
    name = 'dianping.city'
    allowed_domains = ['dianping.com']
    start_urls = ['http://api.t.dianping.com/n/base/cities.xml']

    def parse(self,response):
        xxs = XmlXPathSelector(response)
        citys = xxs.select('//citys');
        for city in citys:
            print city.select('city/name/text()').extract();

class GoodsSpider(BaseSpider):
    name = 'dianping.goods'
    allowed_domains = ['dianping.com']
    start_urls = ['http://api.t.dianping.com/n/api.xml']

    def parse(self,response):
        filename = '../xmls/dianping/goods.xml'
        open(filename,'wb').write(response.body);
