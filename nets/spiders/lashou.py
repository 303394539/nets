
from scrapy.spider import BaseSpider

class CitySpider(BaseSpider):
    name = 'lashou.city'
    allowed_domains = ['lashou.com']
    start_urls = ['http://open.lashou.com/opendeals/lashou/city.xml']

    def parse(self,response):
        filename = '../xmls/lashou/city.xml'
        open(filename,'wb').write(response.body);


class GoodsSpider(BaseSpider):
    name = 'lashou.goods'
    allowed_domains = ['lashou.com']
    start_urls = ['http://open.lashou.com/opendeals/lashou/2419.xml']

    def parse(self,response):
        filename = '../xmls/lashou/beijing.xml'
        open(filename,'wb').write(response.body);
