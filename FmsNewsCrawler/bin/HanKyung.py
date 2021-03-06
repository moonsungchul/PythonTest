
from bs4 import BeautifulSoup
import requests
import configparser
import json

from HtmlParser import HtmlParser
from CrawlerNewspaper import CrawlerNewspaper
from Article import Article
from PulsarStore import PulsarStore

class HanKyung:
    """
    한국 경제 신문을 크롤링한다. 
    """

    def __init__(self, conf):
        self.url1 = "https://www.hankyung.com/finance/0104"
        self.url2 = "https://www.hankyung.com/finance/0103"
        self.url3 = "https://www.hankyung.com/finance/0102"
        self.conf = conf
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
            if 'finance/article' in ss and "#" not in ss:
                aa = v.get("href")
                buf.append(str(aa))
        return buf

    def getStringFilter(self, ss):
        ss = ss.replace("'", "\'")
        return ss

    def parsingNews(self, url):
        ret = []
        links = self.parseLinkArtcle(url)
        for v in links:
            (title, text) = self.news.crawling(v)
            art = Article(self.getStringFilter(title), self.getStringFilter(text), "한국경제")
            print("title : ", title)
            print("text : ", text)
            ret.append(art.toDic())
        return ret

    def crawling(self):
        wp = open("test.jsonl", 'w')
        ret = self.parsingNews(self.url1)
        ret.extend(self.parsingNews(self.url2))
        ret.extend(self.parsingNews(self.url3))

        cl = self.pulsar.getClient()
        pro = self.pulsar.createProcuder(cl, "newspaper")
        for dd in ret:
            jj = json.dumps(dd)
            print("send data : ", jj)
            wp.write(jj + "\n")
            pro.send(jj.encode('utf-8'))
        wp.close()
        cl.close()

        
if __name__ == '__main__':
    conf = {}
    conf['pulsar'] = {"ip":"localhost", "port":6650}
    rr = HanKyung(conf)
    rr.crawling()
