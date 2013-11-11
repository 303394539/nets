
from scrapy.spider import BaseSpider

class CitySpider(BaseSpider):
    name = 'nuomi.city'
    allowed_domains = ['nuomi.com']
    start_urls = ['http://www.nuomi.com/api/dailydeal']

    def parse(self,response):
        filename = '../xmls/nuomi/city.xml'
        open(filename,'wb').write(response.body);


class GoodsSpider(BaseSpider):
    name = 'nuomi.goods'
    allowed_domains = ['nuomi.com']
    start_urls = ['http://www.nuomi.com/api/dailydeal?version=v1']

    def parse(self,response):
        filename = '../xmls/nuomi/goods.xml'
        open(filename,'wb').write(response.body);
