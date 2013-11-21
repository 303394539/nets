# -*- coding:utf-8 -*-

import MySQLdb
from config import DB

class movieMatcher:
    def __init__(self):
        self.cur = MySQLdb.connect(host=DB.HOST,user=DB.USER,passwd=DB.PASSWD,db=DB.NAME,charset=DB.CHARSET).cursor()
        self.sDouban_cache = 'select douban_id,search from douban_cache'
        self.sMovie_mtime = 'select id,`name` from movie_mtime'
        self.sMovie_gewara = 'select id,`name` from movie_gewara'
        self.iMmovie_matcher = 'insert into mmovie_matcher(douban_id)'

    def mmovie_matcher(self):
        self.cur.execute(self.sDouban_cache)
        for row in self.cur.fetchall():
            print row[1]

    def gmovie_matcher(self):
        pass


if __name__=='__main__':
    mm = movieMatcher()
    mm.mmovie_matcher()
