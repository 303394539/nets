# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from scrapy.spider import BaseSpider
from nets import connect
from scrapy import log
import time
import os

class MyBaseSpider(BaseSpider):
    cur = connect()

    def __init__(self):#{{{
        self.path = os.path.abspath('../')
        self.path_image_src = self.path+'/poster/src/'
        self.path_image_rel = self.path+'/poster/release/'
        self.image_size = (320,480)
        LOG = self.path+'/log/'+self.name+'.log'
        ERR = self.path+'/log/'+self.name+'.err'
        INF = self.path+'/log/'+self.name+'.info'
        WAR = self.path+'/log/'+self.name+'.warning'
        log.start(LOG,loglevel=log.DEBUG)
        log.start(ERR,loglevel=log.ERROR)
        log.start(INF,loglevel=log.INFO)
        log.start(WAR,loglevel=log.WARNING)
        self.date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        self.iCity_mtime = 'insert into city_mtime(id,`name`,en)values(%s,%s,%s)'
        self.sCity_mtime = 'select id,`name`,en from city_mtime'
        self.iCinema_mtime = 'insert into cinema_mtime(id,`name`,city_id)values(%s,%s,%s)'
        self.sCinema_mtime = 'select id,`name`,city_id from cinema_mtime'
        self.sMovie_mtime = 'select id,`name`,url from movie_mtime'
        self.iMovie_mtime = 'insert into movie_mtime(id,`name`,url)values(%s,%s,%s)'
        self.iShowtime_mtime = 'insert into showtime_mtime(cinema_id,movie_id,`date`,showtime)values(%s,%s,%s,%s)'
        self.iCity_gewara = 'insert into city_gewara(`name`,en)values(%s,%s)'
        self.sCity_gewara = 'select id,`name`,en from city_gewara'
        self.iCinema_gewara = 'insert into cinema_gewara(id,`name`,city_en)values(%s,%s,%s)'
        self.sCinema_gewara = 'select id,`name`,city_en from cinema_gewara'
        self.sMovie_gewara = 'select id,`name`,url from movie_gewara'
        self.iMovie_gewara = 'insert into movie_gewara(id,`name`,url)values(%s,%s,%s)'
        self.iShowtime_gewara = 'insert into showtime_gewara(cinema_id,movie_id,`date`,showtime)values(%s,%s,%s,%s)'
        self.iMovie_douban = 'insert into movie_douban(id,`name`,directors,actors,`release`,duration,`source`,pid,detail,`types`,grade)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.sMovie_douban = 'select id,`source`,pid,`replace` from movie_douban'
        self.uMovie_douban = 'update movie_douban set grade = %s'
        self.dMovie_douban = 'delete from movie_douban where `source`=%s and pid=%s'
        self.truncateSQLs = {
            'showtime_time':'truncate table showtime_mtime'
        }
    #}}}
    def truncate(self,tables=[]):#{{{
        if len(tables)<=0:return
        for table in tables:
            self.cur.execute(self.truncateSQLs.get(table))
    #}}}
