

#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, Integer, String, Sequence

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class NewsSite(db.Model):
    
    __tablename__ = 'NewsSite'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    url = Column(String(1000))
    down_time = Column(String(100))   # crawling 한 시간 
    crawling_sw = Column(Boolean)

    def __init__(self, name, url, dtime, cr_sw):
        self.name = name
        self.url = url
        self.down_time = dtime
        self.crawling_sw = cr_sw

    def __repr__(self):
        return "<NewsSite('%s', '%s', '%s', '%s',  '%s')>" % \
                (self.id, self.name, self.url,  \
                self.down_time, self.crawling_sw)

    

    