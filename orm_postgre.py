#!/usr/bin/env python
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db = create_engine('postgresql://pguser:Lyreco157@localhost:5433/mock_development', echo=False)
Base = declarative_base(db)

def loadSession():
    """ Load the session """
    metadata = Base.metadata
    Session = sessionmaker(bind=db)
    session = Session()
    return session
    
class Item(Base):
    """ Database model of Item """
    __tablename__ = 'items'
    __table_args__ = {'autoload':True}
    index = Column('id', Integer, primary_key=True)
    title = Column('title', String(200))
    content = Column('content', String(200))

    def __init__(self, itemid, imageurl, localurl=None):
        self.index = index
        self.title = title
        self.content = content

    def __repr__(self):
        return "<Item(id='%d', title='%s', content='%s')>" % (
                self.index, self.title, self.content)

session = loadSession()

products = session.query(Item).all()
print len(products)
# print products[1]

session.close()