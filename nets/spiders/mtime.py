from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from nets.spiders import MyBaseSpider
import json
import subprocess

class ShowtimeSpider(MyBaseSpider):#{{{
    allowed_domains = ['theater.mtime.com']
    download_delay = 3
    download_timeout = 15
    name = 'mtime.showtime'
    base = 'http://service.theater.mtime.com/service/showtime.ms?'
    base += '&Ajax_CallBack=true'
    base += '&Ajax_CallBackMethod=GetTheaterDateShowtimes'
    base += '&Ajax_CallBackType=Mtime.Showtime.Pages.ShowtimeService'
    base += '&Ajax_CallBackArgument0=1'
    base += '&Ajax_CallBackArgument1={0}'
    base += '&Ajax_CallBackArgument5={1}%2000%3A00'
    base += '&Ajax_CallBackArgument6=8'
    base += '&Ajax_CallBackArgument7=0'
    base += '&Ajax_CallBackArgument8=31'
    base += '&Ajax_CallBackArgument9=59'
    base += '&Ajax_CallBackArgument10=1'

    def start_requests(self):#{{{
        self.truncate(tables=['showtime_time'])
        self.cur.execute(self.sCinema_mtime)
        for row in self.cur.fetchall():
            req = Request(self.base.format(row[0],self.date),callback=self.parsePage)
            req.meta['cinema_id']= row[0]
            yield req
    #}}}
        
    def parsePage(self,response):#{{{
        cinema_id = response.meta['cinema_id']
        self.cur.execute(self.sMovie_mtime)
        movie_ids = [row[0] for row in self.cur.fetchall()]
        str = response.body
        str += 'console.log(JSON.stringify(getTheaterDateShowtimesResult.value.showtimeList))'
        p = subprocess.Popen('node',stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        showtime = p.communicate(input=str)[0].replace('\\','')
        hxs = HtmlXPathSelector(response.replace(body=showtime))
        movies = hxs.select('//dl[@class="s_cinamelist"]/dd//div[@class="td pl15"]')
        moviesjson = {}
        showtimes = []
        for movie in movies:
            url = movie.select('./div[1]//h3/a/@href').extract()[0]
            movie_id = int(url.split('/')[-2])
            name = movie.select('./div[1]//h3/a/text()').extract()[0]
            if movie_id:
                if int(movie_id) not in movie_ids:moviesjson[movie_id]=[movie_id,name,url]
            showtime = movie.select('./ul/li/a/b/strong/text()').extract()
            if movie_id:showtimes.append([cinema_id,movie_id,self.date,json.dumps(showtime)])
        self.cur.executemany(self.iMovie_mtime,moviesjson.values())
        self.cur.executemany(self.iShowtime_mtime,showtimes)
        #}}}
#}}}
class CitysAndCinemasSpider(MyBaseSpider):#{{{
    name = 'mtime.cc'
    allowed_domains = ['static1.mtime.cn']
    download_delay = 3
    download_timeout = 15
    start_urls = ['http://static1.mtime.cn/Utility/Data/TheaterListBoxData.m']

    def parse(self,response):#{{{
        str = response.body
        str += 'console.log(JSON.stringify(threaterListBoxData.locations.List))'
        p = subprocess.Popen('node',stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        cache = p.communicate(input=str)[0]
        data = json.loads(cache)
        self.cur.execute(self.sCity_mtime)
        city_ids = [row[0] for row in self.cur.fetchall()]
        self.cur.execute(self.sCinema_mtime)
        cinema_ids = [row[0] for row in self.cur.fetchall()]
        citys = []
        cinemas = []
        for city in data:
            if city.get('Id') not in city_ids:citys.append([city.get('Id'),city.get('NameCn'),city.get('NameEn')])
            if city.get('Cinemas').get('List'):
                for cinema in city.get('Cinemas').get('List'):
                    if cinema.get('Id') not in cinema_ids:cinemas.append([cinema.get('Id'),cinema.get('NameCn'),cinema.get('CityId')])
            if city.get('Districts').get('List'):
                for dis in city.get('Districts').get('List'):
                    if dis.get('Cinemas').get('List'):
                        for cinema in dis.get('Cinemas').get('List'):
                            if cinema.get('Id') not in cinema_ids:cinemas.append([cinema.get('Id'),cinema.get('NameCn'),cinema.get('CityId')])
        self.cur.executemany(self.iCity_mtime,citys)
        self.cur.executemany(self.iCinema_mtime,cinemas)
    #}}}
#}}}
