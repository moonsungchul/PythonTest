
from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DBStore import DBStore
import DBModel
from InfluxStore import InfluxStore 
from InfluxLogger import InfluxLogger
import configparser

class CrawlerManager:

    def __init__(self, conf, dbstore):
        self.conf = conf
        self.dbstore = dbstore
        self.influx = InfluxStore(conf['influx']['host'], conf['influx']['port']) 
        self.influx.switchDB(conf['influx']['dbname'])
        self.logger = InfluxLogger(self.influx) 
        

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./news_crawler.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    DBModel.db.init_app(app)
    app.app_context().push()
    DBModel.db.create_all()

    store = DBStore(DBModel.db)
    cc = "../conf/config.conf"
    conf = configparser.ConfigParser()
    conf.read(cc)
    obj = CrawlerManager(conf, store)
    


