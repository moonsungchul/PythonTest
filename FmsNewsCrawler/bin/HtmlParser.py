
from bs4 import BeautifulSoup
import requests
import configparser

class HtmlParser:

    def __init__(self, conf):
        self.conf = conf 


    def parseAList(self, url):
        buf = []
        html = self.getHtml(url)
        soup = BeautifulSoup(html, 'html.parser')
        ar = soup.find_all('a')
        for v in ar:
            ss = str(v)
            if 'finance/article' in ss and "#" not in ss:
                aa = v.get("href")
                buf.append(str(aa))
        return buf

    def getHtml(self, url):
        html = ""
        resp = requests.get(url)
        if resp.status_code == 200:
            html = resp.text
        return html


    def test(self):
        url = "https://www.hankyung.com/finance/0104"
        self.parseAList(url)

if __name__ == '__main__':
    cc = "../conf/config.conf"
    conf = configparser.ConfigParser()
    conf.read(cc)
    html = HtmlParser(conf)
    html.test()
    
