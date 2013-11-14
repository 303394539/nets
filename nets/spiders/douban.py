# -*- coding:utf8 -*-
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from nets.spiders import MyBaseSpider
import json
import subprocess

class MovieSpider(MyBaseSpider):#{{{
    allowed_domains = ['movie.douban.com']
    download_delay = 3
    download_timeout = 15
    name = 'douban.movie'
    base = 'http://movie.douban.com/subject_search?search_text={0}'

    def start_requests(self):#{{{
        datas = []
        self.cur.execute(self.sMovie_gewara)
        for row in self.cur.fetchall():
            data = [r for r in row]
            data.append('gewara')
            datas.append(data)
        self.cur.execute(self.sMovie_mtime)
        for row in self.cur.fetchall():
            data = [r for r in row]
            data.append('mtime')
            datas.append(data)
        for d in datas:
            req = Request(self.base.format(d[1].encode('utf-8')),callback=self.parsePage)
            req.meta['source'] = d[3]
            req.meta['pid'] = d[0]
            req.meta['view'] = u'search'
            yield req
    #}}}
        
    def parsePage(self,response):#{{{
        source = response.meta['source']
        pid = response.meta['pid']
        view = response.meta['view']
        if view == 'search':
            hxs = HtmlXPathSelector(response.replace(body=response.body))
            movie = hxs.select('//table[1]/tr/td[2]/div/a')
            if movie:
                href = movie.select('./@href').extract()[0]
                req = Request(href,callback=self.parsePage)
                req.meta['id'] = href.split('/')[2]
                req.meta['source'] = source
                req.meta['pid'] = pid
                req.meta['view'] = u'movie'
                yield req
        elif view == 'movie':
            id = response.meta['id']
            hxs = HtmlXPathSelector(response.replace(body=response.body))
            namespan = hxs.select('//div[@id="content"]/h1/span[1]')
            if namespan:name = namespan.select('./text()').extract()[0].split(' ')[0]
            print name
            movie = hxs.select('//div[@class="article"]')
            spans = movie.select('./div/div/div/div[2]/span')
            directors = []
            actors = []
            types = []
            releases = []
            movies = []
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
            detailspan = movie.select('./div/div/span[@property="v:summary"]')
            if detailspan:detail = detailspan.select('./text()').extract()[0]
            else:
                detailspan = movie.select('./div/div/span/span[@property="v:summary"]')
                if detailspan:detail = detailspan.select('./text()').extract()[0]
            director = ''
            for d in directors[:-1]:
                director += d+'/'
            director += directors[-1]
            actor = ''
            for a in actors[:-1]:
                actor += a+'/'
            actor += actors[-1]
            type = ''
            for t in types[:-1]:
                type += t+'/'
            type += types[-1]
            image = movie.select('./div/div/div/div/a[@class="nbgnbg"]/@href').extract()[0]
            if 'lpic' in image:
                req = Request(image,callback=self.parsePage)
                req.meta['source'] = source
                req.meta['pid'] = pid
                req.meta['view'] = u'image'
                yield req
            else:
                req = Request(image,callback=self.parsePage)
                req.meta['source'] = source
                req.meta['pid'] = pid
                req.meta['view'] = u'images'
                yield req
        #}}}
#}}}
