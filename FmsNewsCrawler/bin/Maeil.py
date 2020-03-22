from bs4 import BeautifulSoup
import requests
import configparser
import json

from HtmlParser import HtmlParser
from CrawlerNewspaper import CrawlerNewspaper
from Article import Article
from PulsarStore import PulsarStore
from Utils import Utils

class Maeil:
    """
    매일 경제 신문을 크롤링한다. 
    """

    def __init__(self, conf):
        self.url1 = "https://www.mk.co.kr/news/economy"
        self.conf = conf
        self.html= HtmlParser(conf)
        self.news = CrawlerNewspaper(conf)
        self.pulsar = PulsarStore(conf['pulsar']['ip'], conf['pulsar']['port'])
        self.util = Utils()

    def parseLinkArtcle(self, url):
        buf = []
        doc = self.html.getHtml(url)
        soup = BeautifulSoup(doc, 'html.parser')
        ar = soup.find_all('a')
        for v in ar:
            ss = str(v)
            if "view" in ss:
                aa = v.get("href")
                if "news/economy" in aa or "news/stock" in aa:
                    buf.append(str(aa))
        return buf


    def parsingNews(self, url):
        ret = []
        links = self.parseLinkArtcle(self.url1)
        for v in links:
            try:
                (title, text) = self.news.crawling(v)
                print('title : ', title)
                print("text : ", text)
                art = Article(self.util.getStringFilter(title), self.util.getStringFilter(text), "매일경제")
                ret.append(art.toDic())
            except:
                print('new crawling error ')
        return ret


    def crawling(self):
        ret = self.parsingNews(self.url1)
        print(ret)
        cl = self.pulsar.getClient()
        pro = self.pulsar.createProcuder(cl, "newspaper")
        for dd in ret:
            jj = json.dumps(dd)
            print("send data : ", jj)
            pro.send(jj.encode('utf-8'))
        cl.close()



if __name__ == '__main__':
    conf = {}
    conf['pulsar'] = {"ip":"172.17.0.5", "port":6650}
    rr = Maeil(conf)
    rr.crawling()



        