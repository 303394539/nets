# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from scrapy.spider import BaseSpider
from nets import connect
import time

class MyBaseSpider(BaseSpider):
    cur = connect()

    def __init__(self):#{{{
        self.date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        self.iCity_mtime = 'insert into city_mtime(id,`name`,en)values(%s,%s,%s)'
        self.sCity_mtime = 'select id,`name`,en from city_mtime'
        self.iCinema_mtime = 'insert into cinema_mtime(id,`name`,string_id,city_id)values(%s,%s,%s,%s)'
        self.sCinema_mtime = 'select id,`name`,string_id,city_id from cinema_mtime'
        self.sCinema_mtime_havestr = "select id,`name`,string_id from cinema_mtime where string_id != '' limit 1"
        self.sMovie_mtime = 'select id,`name`,url from movie_mtime'
        self.iMovie_mtime = 'insert into (id,`name`,url)values(%s,%s,%s)'
        self.iShowtime_mtime = 'insert into(cinema_id,movie_id,date,showtime)values(%s,%s,%s,%s,%s)'
        self.truncateSQLs = {
            'showtime_time':'truncate table showtime_mtime'
        }
    #}}}
    def truncate(self,tables=[]):#{{{
        if len(tables)<=0:return
        for table in tables:
            self.cur.execute(self.truncateSQLs.get(table))
    #}}}
