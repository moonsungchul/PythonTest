from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import DBModel



class DBStore:

    def __init__(self, db, app):
        self.db = db
        self.app = app

    def insert(self, obj):
        with app.app_context():
            self.db.session.add(obj)
            self.db.session.commit()

    def commit(self):
        with app.app_context():
            self.db.session.commit()

    def test(self):
        user = DBModel.NewsSite("mm", "url", "2020-03-20")
        print(user)
        self.insertUser(user)

    def saveInitData(self):
        news1 = DBModel.NewsSite("한국경제", "https://www.hankyung.com", "2020-03-25 22:20:00", True)
        news2 = DBModel.NewsSite("매일경제", "https://www.mk.co.kr/news", "2020-03-25 22:20:00", True)
        self.insert(news1)
        self.insert(news2)


    def getNewsSites(self):
        with app.app_context():
            return self.db.session.query(DBModel.NewsSite).all()


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./news_crawler.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    DBModel.db.init_app(app)
    app.app_context().push()
    DBModel.db.create_all()

    store = DBStore(DBModel.db)
    #store.test()
    store.saveInitData()
    store.getNewsSites()

    



        
        


