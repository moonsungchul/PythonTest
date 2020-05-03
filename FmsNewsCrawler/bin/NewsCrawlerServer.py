
import schedule
import time
from flask import Flask
from flask_restful import Resource, Api
import DBModel
from DBStore import DBStore
from CrawlingSchedule import CrawlingSchedule  
import configparser
from CrawlerManager import CrawlerManager

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./news_crawler.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

DBModel.db.init_app(app)
app.app_context().push()

DBModel.db.create_all()
dbstore = DBStore(DBModel.db, app)

conf = configparser.ConfigParser()
conf.read("../conf/config.conf")

manager = CrawlerManager(conf, dbstore)
crawler = CrawlingSchedule(manager)


if __name__ == '__main__':
    print("Start News papaper Crawling Server ...")
    manager.logger.info("SERVER", "Crawling Server start")
    crawler.start()
    app.run(debug=True)
    
