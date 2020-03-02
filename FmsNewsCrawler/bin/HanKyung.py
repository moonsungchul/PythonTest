
from bs4 import BeautifulSoup
import requests
import configparser

from HtmlParser import HtmlParser
from CrawlerNewspaper import CrawlerNewspaper

class HanKyung:

    def __init__(self, conf):
        self.url1 = "https://www.hankyung.com/finance/0104"
        self.url2 = "https://www.hankyung.com/finance/0103"
        self.url3 = "https://www.hankyung.com/finance/0102"
        self.conf = conf
        self.html = HtmlParser(conf)
        self.news = CrawlerNewspaper(conf)


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
            print("title : ", title)
            print("text : ", text)
            ret.append((self.getStringFilter(title), self.getStringFilter(text)))
        return ret

    def test(self):
        ret = self.parsingNews(self.url1)
        print("ret : ", ret)
        ret = self.parsingNews(self.url2)
        print("ret : ", ret)
        ret = self.parsingNews(self.url3)
        print("ret : ", ret)

        
if __name__ == '__main__':
    cc = "../conf/config.conf"
    conf = configparser.ConfigParser()
    conf.read(cc)
    rr = HanKyung(conf)
    rr.test()
