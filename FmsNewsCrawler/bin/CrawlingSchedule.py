
from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from HanKyung import HanKyung
from Maeil import Maeil
from DBStore import DBStore 
import DBModel
import datetime, time
import schedule
import threading, requests, time
import random
from CrawlerManager import CrawlerManager
import configparser

class CrawlingSchedule(threading.Thread):

    #def __init__(self, db, conf):
    def __init__(self, manager):
        threading.Thread.__init__(self)
        self.conf = manager.conf
        self.store = manager.dbstore
        self.logger = manager.logger
        self.hankyung = HanKyung(self.conf)
        self.maeil = Maeil(self.conf)

        self.today_hour = 10
        self.thread_sw = True
        self.last_crawling = datetime.datetime(2000, 1,1, 00,00,00)
        self.crawling_sw = False
        self.crawling_count = 0
        

    def job(self):
        today = datetime.datetime.now()
        dif = today - self.last_crawling
        if dif.days > 1:
            self.today_hour = random.randint(1, 23)
            self.last_crawling = datetime.datetime.now()
            self.crawling_sw = True
            self.crawling_count = 0


        if self.crawling_sw == True and self.crawling_count == self.today_hour:
            print("crawling .........  ", self.crawling_count, self.today_hour)
            self.crawling_sw = False
            arts = self.store.getNewsSites()
            for v in arts:
                if v.crawling_sw == True:
                    if v.name == "한국경제":
                        self.hankyung.crawling()
                        print("downlaod hanyung ...")
                        v.down_time = str(datetime.datetime.now())
                        self.store.commit()
                    
                    elif v.name == "매일경제":
                        self.maeil.crawling()
                        print("downlaod maeil ...")
                        v.down_time = str(datetime.datetime.now())
                        self.store.commit()
        self.crawling_count += 1
        print("crawling self.crawing_count ", self.crawling_count)


    def stopThread(self):
        self.thread_sw = False


    def run(self):
        schedule.every().hour.do(self.job)
        while self.thread_sw:
            print("thread pending ...")
            schedule.run_pending()
            time.sleep(600)


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./news_crawler.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    DBModel.db.init_app(app)
    app.app_context().push()
    DBModel.db.create_all()

    #conf = {}
    #conf['pulsar'] = {"ip":"172.17.0.5", "port":6650}
    conf = configparser.ConfigParser() 
    conf.read("../conf/config.conf")

    store = DBStore(DBModel.db )
    manager = CrawlerManager(conf, store)

    rr = CrawlingSchedule(manager)
    #rr.job()
    rr.start()

    time.sleep(200)
    rr.stopThread()

