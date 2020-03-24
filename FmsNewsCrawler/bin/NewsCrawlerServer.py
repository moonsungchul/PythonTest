
from flask import Flask
from flask_restful import Resource, Api
import DBModel
from DBStore import DBStore


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./news_crawler.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
DBModel.db.init_app(app)
app.app_context().push()
DBModel.db.create_all()

dbstore = DBStore(DBModel.db)

if __name__ == '__main__':
    print("Start News papaper Crawling Server ...")
    app.run(debug=True)
    


