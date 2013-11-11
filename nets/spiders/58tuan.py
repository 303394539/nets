
from scrapy.spider import BaseSpider

class CitySpider(BaseSpider):
    name = '58tuan.city'
    allowed_domains = ['58.com']
    start_urls = ['http://open.t.58.com/api/citys']

    def parse(self,response):
        filename = '../xmls/58tuan/city.xml'
        open(filename,'wb').write(response.body);


class GoodsSpider(BaseSpider):
    name = '58tuan.goods'
    allowed_domains = ['58.com']
    start_urls = ['http://open.t.58.com/api/products']

    def parse(self,response):
        filename = '../xmls/58tuan/goods.xml'
        open(filename,'wb').write(response.body);
