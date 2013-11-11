
from scrapy.spider import BaseSpider

class CitySpider(BaseSpider):
    name = '55tuan.city'
    allowed_domains = ['55tuan.com']
    start_urls = ['http://www.55tuan.com/partner/city/wowoCity.xml']

    def parse(self,response):
        filename = '../xmls/55tuan/city.xml'
        open(filename,'wb').write(response.body);


class GoodsSpider(BaseSpider):
    name = '55tuan.goods'
    allowed_domains = ['55tuan.com']
    start_urls = ['http://www.55tuan.com/partner/partnerApi?partner=wowo']

    def parse(self,response):
        filename = '../xmls/55tuan/goods.xml'
        open(filename,'wb').write(response.body);
