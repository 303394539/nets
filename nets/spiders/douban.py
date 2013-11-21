# -*- coding:utf8 -*-
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from nets.spiders import MyBaseSpider
import json
import subprocess
import Image

class MovieSpider(MyBaseSpider):#{{{
    allowed_domains = ['douban.com']
    download_delay = 2
    download_timeout = 30
    name = 'douban.movie'

    def start_requests(self):#{{{
        self.cur.execute(self.sMmovie_matcher)
        mmovie_matcher = self.cur.fetchall()
        douban_ids_matcher = [row[0] for row in mmovie_matcher]
        mmovie_ids = [row[1] for row in mmovie_matcher]
        self.cur.execute(self.sGmovie_matcher)
        gmovie_matcher = self.cur.fetchall()
        douban_ids_matcher += [row[0] for row in gmovie_matcher]
        gmovie_ids = [row[1] for row in gmovie_matcher]
        douban_ids_matcher = list(set(douban_ids_matcher))
        self.cur.execute(self.sMovie)
        douban_ids = [row[0] for row in self.cur.fetchall()]
        #判断人为修改的新douban_id是否已经爬取，如果没有重启爬取
        for douban_id in douban_ids_matcher:
            if douban_id not in douban_ids:
                req = Request(self.douban_movie_url.format(douban_id),callback=self.parseMovie)
                req.meta['douban_id'] = douban_id
                yield req
        #判断电影关联是否存在，如果不存在重新爬取
        self.cur.execute(self.sMovie_mtime)
        for row in self.cur.fetchall():
            if row[0] not in mmovie_ids:
                req = Request(self.douban_search_url.format(row[1].encode('utf-8')),callback=self.parseSearch)
                req.meta['search'] = row[1]
                yield req
        self.cur.execute(self.sMovie_gewara)
        for row in self.cur.fetchall():
            if row[0] not in gmovie_ids:
                req = Request(self.douban_search_url.format(row[1].encode('utf-8')),callback=self.parseSearch)
                req.meta['search'] = row[1]
                yield req
    #}}}

    def parseSearch(self,response):#{{{
        search = response.meta['search']
        hxs = HtmlXPathSelector(response.replace(body=response.body))
        movie = hxs.select('//table[1]/tr/td[2]/div/a')
        if movie:
            href = movie.select('./@href').extract()[0]
            douban_id = int(href.split('/')[4])
            self.cur.execute(self.iDouban_cache,(douban_id,search))
            req = Request(href,callback=self.parseMovie)
            req.meta['douban_id'] = douban_id
            yield req
    #}}}
    
    def parseMovie(self,response):#{{{
        douban_id = response.meta['douban_id']
        hxs = HtmlXPathSelector(response.replace(body=response.body))
        movie = hxs.select('//div[@class="article"]')
        self.cur.execute(self.sMovie)
        douban_ids = [row[0] for row in self.cur.fetchall()]
        if douban_id in douban_ids:
            grade = '6'
            gradestrong = movie.select('./div/div/div[2]/div/p/strong/text()')
            if gradestrong:grade = gradestrong.extract()[0]#评分
            self.cur.execute(self.uMovie,(grade,douban_id))
        else:
            namespan = hxs.select('//div[@id="content"]/h1/span[1]')
            if namespan:name = namespan.select('./text()').extract()[0].split(' ')[0]#电影名称
            grade = '6'
            gradestrong = movie.select('./div/div/div[2]/div/p/strong/text()')
            if gradestrong:grade = gradestrong.extract()[0]#评分
            spans = movie.select('./div/div/div/div[2]/span')
            directors = []#导演
            actors = []#演员
            types = []#类型
            releases = []#首映时间
            duration = 90
            for span in spans:
                s = span.select('./span[@class="pl"]')
                if s:
                    peoples = span.select('./a')
                    for p in peoples:
                        text = p.select('./text()').extract()[0]
                        href = p.select('./@href').extract()
                        if href:
                            if 'celebrity' in href[0]:
                                if p.select('./@rel'):
                                    directors.append(text)
                                else:
                                    actors.append(text)
                else:
                    property = span.select('./@property')
                    if property:
                        text = property.extract()[0]
                        if 'genre' in text:
                            types.append(span.select('./text()').extract()[0])
                        elif 'initialReleaseDate' in text:
                            releases.append(span.select('./text()').extract()[0].split('(')[0])
                        elif 'runtime' in text:
                            duration = span.select('./@content').extract()[0]
            detail = ''
            detailspan = movie.select('./div/div/span[@property="v:summary"]')
            if detailspan:detail = detailspan.select('./text()').extract()[0]
            else:
                detailspan = movie.select('./div/div/span/span[@property="v:summary"]')
                if detailspan:detail = detailspan.select('./text()').extract()[0].strip()#简介
            director = ''
            if directors:
                for d in directors[:-1]:
                    director += d+'/'
                director += directors[-1]
            actor = ''
            if actors:
                for a in actors[:-1]:
                    actor += a+'/'
                actor += actors[-1]
            type = ''
            if types:
                for t in types[:-1]:
                    type += t+'/'
                type += types[-1]
            release = 0
            if releases:release=releases[0]
            self.cur.execute(self.iMovie,(douban_id,name,director,actor,release,duration,detail,type,grade))
            image = movie.select('./div/div/div/div/a[@class="nbgnbg"]/@href').extract()[0]
            if 'lpic' in image:
                req = Request(image,callback=self.parseImage)
                req.meta['douban_id'] = douban_id
                yield req
            else:
                req = Request(image,callback=self.parseImageList)
                req.meta['douban_id'] = douban_id
                yield req
            
    #}}}

    def parseImageList(self,response):#{{{
        douban_id = response.meta['douban_id']
        hxs = HtmlXPathSelector(response.replace(body=response.body))
        images = hxs.select('//div[@class="article"]/ul/li')
        result = []#result[(ratio),是否(正式或中国),url]
        for img in images:
            c = img.select('./@class')
            urllist = img.select('./div[@class="cover"]/a/@href')
            ratiolist = img.select('./div[@class="prop"]/text()')
            namelist = img.select('./div[@class="name"]/text()')
            if c:
                if c.extract()[0] == u'sep':
                    continue
            url = urllist.extract()[0].strip()
            ratio = ratiolist.extract()[0].strip().split('x')
            x = int(ratio[0])
            y = int(ratio[1])
            name = namelist.extract()[0].strip()
            cache = [(x,y),0,url]
            if u'正式' in name:cache[1]=1
            if u'中国' in name:cache[1]=2
            if u'正式' in name and u'中国' in name:cache[1]=3
            if result:
                if y>x:
                    if cache[1]>result[1]:result = cache
                    elif cache[1]==result[1]:
                        if (x+y)>(result[0][0]+result[0][1]):result = cache
                        elif result[0][0]>=result[0][1]:result = cache
            else:
                result = cache
        req = Request(result[2],callback=self.parseImageView)
        req.meta['douban_id'] = douban_id
        yield req
    #}}}

    def parseImageView(self,response):#{{{
        douban_id = response.meta['douban_id']
        hxs = HtmlXPathSelector(response.replace(body=response.body))
        image = hxs.select('//div[@class="photo-wp"]/a[@class="photo-zoom"]/@href').extract()[0].strip()
        req = Request(image,callback=self.parseImage)
        req.meta['douban_id'] = douban_id
        yield req
    #}}}
    
    def parseImage(self,response):#{{{
        douban_id = response.meta['douban_id']
        name = str(douban_id)+'.jpg'
        open(self.path_image_src+name,'wb').write(response.body)
        img = Image.open(self.path_image_src+name)
        img.resize(self.image_size,Image.ANTIALIAS).save(self.path_image_rel+name,'JPEG')
    #}}}
        
#}}}
