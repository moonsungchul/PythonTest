
from bs4 import BeautifulSoup
import requests
import configparser
import json

from HtmlParser import HtmlParser
from CrawlerNewspaper import CrawlerNewspaper
from Article import Article
from PulsarStore import PulsarStore


class FETimes:
    """
    금융경제신문을 크롤링 한다. 
    """

    def __init__(self, conf):
        self.url1 = "http://www.fetimes.co.kr/news/articleList.html?sc_section_code=S1N16&view_type=sm"
        self.url2 = "http://www.fetimes.co.kr/news/articleList.html?sc_section_code=S1N17&view_type=sm"
        self.url3 = "http://www.fetimes.co.kr/news/articleList.html?sc_section_code=S1N18&view_type=sm"
        self.burl = "http://www.fetimes.co.kr"
        self.html = HtmlParser(conf)
        self.news = CrawlerNewspaper(conf)
        self.pulsar = PulsarStore(conf['pulsar']['ip'], conf['pulsar']['port'])

    def parseLinkArtcle(self, url):
        buf = []
        doc = self.html.getHtml(url)
        soup = BeautifulSoup(doc, 'html.parser')
        ar = soup.find_all('a')
        for v in ar:
            ss = str(v)
            if 'news/articleView' in ss:
                aa = v.get("href")
                uu = self.burl + str(aa)
                buf.append(uu)
        return buf

    def getStringFilter(self, ss):
        ss = ss.replace("'", "\'")
        return ss

    def parsingNews(self, url):
        ret = []
        links = self.parseLinkArtcle(url)
        for v in links:
            (title, text) = self.news.crawling(v)
            text = text.replace("저작권자 © 금융경제신문 무단전재 및 재배포 금지", "")
            art = Article(self.getStringFilter(title), self.getStringFilter(text), "한국경제")
            #print("title : ", title)
            #print("text : ", text)
            
            ret.append(art.toDic())
            print(art.toDic())
        return ret

    def crawling(self):
        ret = self.parsingNews(self.url1)
        ret.extend(self.parsingNews(self.url2))
        ret.extend(self.parsingNews(self.url3))
            
        cl = self.pulsar.getClient()
        pro = self.pulsar.createProcuder(cl, "newspaper")
        for dd in ret:
            jj = json.dumps(dd)
            print("send data : ", jj)
            pro.send(jj.encode('utf-8'))
        cl.close()

        
if __name__ == '__main__':
    conf = {}
    conf['pulsar'] = {"ip":"172.17.0.4", "port":6650}
    rr = FETimes(conf)
    rr.crawling()
