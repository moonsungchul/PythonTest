from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import DBModel



class DBStore:

    def __init__(self, db):
        self.db = db

    def insertUser(self, user):
        self.db.session.add(user)
        self.db.session.commit()


    def test(self):
        user = DBModel.NewsSite("mm", "url", "2020-03-20")
        print(user)
        self.insertUser(user)
        


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./news_crawler.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    DBModel.db.init_app(app)
    app.app_context().push()
    DBModel.db.create_all()

    store = DBStore(DBModel.db)
    store.test()



        
        

