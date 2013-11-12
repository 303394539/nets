from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from nets.spiders import MyBaseSpider
import json
import subprocess

class ShowtimeSpider(MyBaseSpider):#{{{
    allowed_domains = ['gewara.com']
    download_delay = 3
    download_timeout = 15
    name = 'gewara.showtime'
    base = 'http://www.gewara.com/cinema/ajax/getCinemaPlayItem.xhtml?cid={0}&fyrq={1}'

    def start_requests(self):#{{{
        pass
    #}}}
        
    def parsePage(self,response):#{{{
        pass
        #}}}
#}}}

class CitysSpider(MyBaseSpider):#{{{
    name = 'gewara.city'
    allowed_domains = ['gewara.com']
    download_delay = 3
    download_timeout = 15
    start_urls = ['http://www.gewara.com/ajax/common/loadHeadCity.xhtml']

    def parse(self,response):#{{{
        hxs = HtmlXPathSelector(response.replace(body=response.body))
        data = hxs.select('//div[@class="ui_city_List none clear"]/div/dl/dd/ul/li')
        citys = []
        for city in data:
            name = city.select('./a/text()').extract()[0]
            en = city.select('./a/@href').extract()[0].split('/')[1]
            citys.append([name,en])
        self.cur.executemany(self.iCity_gewara,citys)
    #}}}
#}}}

class CinemasSpider(MyBaseSpider):#{{{
    name = 'gewara.cinema'
    allowed_domains = ['gewara.com']
    download_delay = 3
    download_timeout = 15
    base = 'http://www.gewara.com/{0}/cinemalist?pageNo={1}'

    def start_requests(self):#{{{
        self.cur.execute(self.sCity_gewara)
        for row in self.cur.fetchall():
            req = Request(self.base.format(row[2],0),callback=self.parsePage)
            req.meta['en'] = row[2]
            req.meta['begin'] = True
            yield req
    #}}}

    def parsePage(self,response):#{{{
        en =  response.meta['en']
        begin = response.meta['begin']
        hxs = HtmlXPathSelector(response.replace(body=response.body))
        if begin:
            data = hxs.select('//div[@class="page"]/div[@id="page"]/a')
            maxpage = 0
            if data:
                maxpage = data[-2].select('./span/text()').extract()[0]
                for i in range(int(maxpage)+1):
                    req = Request(self.base.format(en,i),callback=self.parsePage)
                    req.meta['en'] = en
                    req.meta['begin'] = False
                    yield req
        self.cur.execute(self.sCinema_gewara)
        cinema_ids = [row[0] for row in self.cur.fetchall()]
        data = hxs.select('//div[@class="movieList"]/ul/li/div[@class="ui_media"]/div[@class="ui_pic cinema"]/a')
        cinemas = []
        for cinema in data:
            id = cinema.select('./@href').extract()[0].split('/')[2]
            name = cinema.select('./@title').extract()[0]
            if int(id) not in cinema_ids:cinemas.append([id,name,en])
        self.cur.executemany(self.iCinema_gewara,cinemas)
    #}}}
#}}}
