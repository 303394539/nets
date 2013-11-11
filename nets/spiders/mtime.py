
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from nets.spiders import MyBaseSpider
import json
import subprocess

class ShowtimeSpider(MyBaseSpider):#{{{
    allowed_domains = ['theater.mtime.com']
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
        self.cur.execute(self.sCinema_mtime_havestr)
        for row in self.cur.fetchall():
            req = Request(self.base.format(row[0],self.date),callback=self.parsePage)
            yield req
    #}}}
        
    def parsePage(self,response):#{{{
        str = response.body
        str += 'console.log(JSON.stringify(getTheaterDateShowtimesResult.value.showtimeList))'
        p = subprocess.Popen('node',stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        showtime = p.communicate(input=str)[0].replace('\\','')
        hxs = HtmlXPathSelector(response.replace(body=showtime))
        cinemas = hxs.select('//dl[@class="s_cinamelist"]//dd')
        print cinemas
        for cinema in cinemas:
            url = cinema.select('//h3[@class="yahei fl px20 lh15 normal"]/a[@class="c_000"]/@href').extract()
            name = cinema.select('//h3[@class="yahei fl px20 lh15 normal"]/a[@class="c_000"]/text()').extract()
            print name
            print url
        #}}}
#}}}
class CitysAndCinemasSpider(MyBaseSpider):#{{{
    name = 'mtime.cc'
    allowed_domains = ['static1.mtime.cn']
    download_delay = 3
    download_timeout = 15
    base = 'http://service.theater.mtime.com/service/showtime.ms?'
    base += '&Ajax_CallBack=true'
    base += '&Ajax_CallBackType=Mtime.Theater.Pages.ShowtimeService'
    base += '&Ajax_CallBackMethod=SearchCinemaByMap'
    base += '&Ajax_CallBackArgument0=292'
    base += '&Ajax_CallBackArgument1=0'
    base += '&Ajax_CallBackArgument2='
    base += '&Ajax_CallBackArgument3={0}'
    base += '&Ajax_CallBackArgument4='
    base += '&Ajax_CallBackArgument5=0'
    base += '&Ajax_CallBackArgument6=false'
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
                    if cinema.get('Id') not in cinema_ids:cinemas.append([cinema.get('Id'),cinema.get('NameCn'),'',cinema.get('CityId')])
            if city.get('Districts').get('List'):
                for dis in city.get('Districts').get('List'):
                    string_id = dis.get('StringId')
                    if dis.get('Cinemas').get('List'):
                        for cinema in dis.get('Cinemas').get('List'):
                            if cinema.get('Id') not in cinema_ids:cinemas.append([cinema.get('Id'),cinema.get('NameCn'),string_id,cinema.get('CityId')])
        self.cur.executemany(self.iCity_mtime,citys)
        self.cur.executemany(self.iCinema_mtime,cinemas)
    #}}}
#}}}
