
import configparser
from newspaper import Article


class CrawlerNewspaper:
    """
    지정된 url의 신문 가사를 가져온다. 
    """

    def __init__(self, conf):
        self.conf = conf


    def crawling(self, url):
        print("crawling ....")
        a = Article(url, language='ko')
        a.download()
        a.parse()
        print("title : ", a.title)
        print("text : ", a.text)
        return [a.title, a.text]


    def test(self):
        url = "https://www.hankyung.com/finance/0104"
        self.crawling(url)



if __name__ == '__main__':
    cc = "../conf/config.conf"
    conf = configparser.ConfigParser()
    conf.read(cc)
    rr = CrawlerNewspaper(conf)
    rr.test()
