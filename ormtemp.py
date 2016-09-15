#!/usr/bin/env python
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = create_engine('mysql://outfitter:Ster1ing@localhost:3306/outfitter', echo=False) 
Base = declarative_base(db)

def loadSession():
    """ Load the database session """
    metadata = Base.metadata
    Session = sessionmaker(bind=db)
    session = Session()
    return session

class ProductPrice(Base):
    """ Define the ProductPrice table """
    __tablename__ = "productprices"
    id = Column('id', Integer, primary_key=True)
    productid = Column('productid', Integer)
    price = Column('price', String(50))
    date = Column('checkdate', Date)
    
    def __init__(self, productid, price, date):
        self.productid = productid
        self.price = price
        self.date = date
        
    def __repr__(self):
        return "<ProductPrice(productid='%d', price='%s', date='%s')>" % (
                self.productid, self.price, self.date)

if __name__ == "__main__":
    session = loadSession()
    product_id = 85
    for last_price_entry in session.query(ProductPrice).filter(ProductPrice.productid == product_id).order_by("checkdate desc").limit(1):
        print last_price_entry.price