

from bs4 import BeautifulSoup
import requests
import configparser
import json

from HtmlParser import HtmlParser
from CrawlerNewspaper import CrawlerNewspaper
from Article import Article
from PulsarStore import PulsarStore


class Seoul:
    """
    서울 경제 신문을 크롤링 한다. 
    """
    def __init__(self, conf):
        self.url = "https://m.sedaily.com"
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
            if '/NewsView/' in ss:
                aa = v.get("href")
                hh = self.url +"/" + str(aa)
                buf.append(hh)
        return buf

    def getStringFilter(self, ss):
        ss = ss.replace("'", "\'")
        return ss

    def parsingNews(self, url):
        ret = []
        links = self.parseLinkArtcle(url)
        for v in links:
            print(v)
            (title, text) = self.news.crawling(v)
            art = Article(self.getStringFilter(title), self.getStringFilter(text), "서울경제")
            print("title : ", title)
            print("text : ", text)
            ret.append(art.toDic())
        return ret

    def crawling(self):
        ret = self.parsingNews(self.url)
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
    rr = Seoul(conf)
    rr.crawling()


         
        
