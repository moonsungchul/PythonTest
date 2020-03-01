
import configparser


class CrawlerNewspaper:

    def __init__(self, conf):
        self.conf = conf


    def crawling(self):
        print("crawling ....")



if __name__ == '__main__':
    cc = "../conf/config.conf"
    conf = configparser.ConfigParser()
    conf.read(cc)
    rr = CrawlerNewspaper(conf)
    rr.crawling()
