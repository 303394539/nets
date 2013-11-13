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
        self.cur.execute(self.sCinema_gewara)
        for row in self.cur.fetchall():
            req = Request(self.base.format(row[0],self.date),callback=self.parsePage)
            req.meta['cinema_id']=row[0]
            yield req
    #}}}
        
    def parsePage(self,response):#{{{
        self.cur.execute(self.sMovie_gewara)
        movie_ids = [row[0] for row in self.cur.fetchall()]
        cinema_id = response.meta['cinema_id']
        hxs = HtmlXPathSelector(response.replace(body=response.body))
        data = hxs.select('//div[@class="ticket_choose_box"]/div')
        movies = []
        showtimes = []
        for movie in data[1:]:
            url = movie.select('./div[@class="chooseOpi_movie"]/div[@class="choseMovieInfo"]/div[@class="ui_media"]/div[@class="ui_pic"]/a/@href').extract()[0]
            id = int(url.split('/')[2])
            name = movie.select('./div[@class="chooseOpi_movie"]/div[@class="choseMovieInfo"]/div[@class="ui_media"]/div[@class="ui_pic"]/a/@title').extract()[0]
            if id not in movie_ids:movies.append([id,name,'http://www.gewara.com'+url])
            ss = movie.select('./div[2]/div[@class="chooseOpi_body"]/ul/li/span[@class="opitime"]/b')
            showtime = []
            for s in ss:
                showtime.append([s.select('./text()').extract()[0]])
            showtimes.append([cinema_id,id,self.date,json.dumps(showtime)])
        self.cur.executemany(self.iMovie_gewara,movies)
        self.cur.executemany(self.iShowtime_gewara,showtimes)
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
