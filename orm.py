#!/usr/bin/env python
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker

db = create_engine('mysql://outfitter:6qufMLA2BxmXeqe8@localhost/outfitter', echo=False)
Base = declarative_base(db)

def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=db)
    session = Session()
    return session

class Brand(Base):
    """"""
    __tablename__ = 'brands'
    __table_args__ = {'autoload':True}
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(150))
    logourl = Column('logourl', String(200), nullable=True)
    logolargeurl = Column('logolargeurl', String(200), nullable=True)
    uuid = Column('uuid', String(50))
    
    def __init__(self, name, logourl, logolargeurl, uuid):
        self.name = unicode(name)
        self.logourl = logourl
        self.logolargeurl = logolargeurl
        self.uuid = uuid
        
    def __repr__(self):
        return """<Brand(name='%s',logourl='%s',logolargeurl='%s')>""" % (
                self.name, self.logourl, self.logolargeurl)
    
    def insert(self):
        print "Inserting", self

class Item(Base):
    """"""
    __tablename__ = 'items'
    __table_args__ = {'autoload':True}
    id = Column('id', Integer, primary_key=True)
    storeid = Column('storeid', Integer)
    itemid = Column('itemid', String(50))
    brandid = Column('brandid', Integer)
    link = Column('link', String(200))
    color = Column('color', String(50))
    title = Column('title', String(200))
    category = Column('category', String(200))
    gender = Column('gender', String(20))
    uuid = Column('uuid', String(50))
    
    def __init__(self, storeid, itemid, brandid, link, color, title, category, gender, uuid):
        self.storeid = int(storeid)
        self.itemid = itemid
        self.brandid = int(brandid)
        self.link = link
        self.color = color
        self.title = title
        self.category = category
        self.gender = gender
        self.uuid = uuid
        
    def __repr__(self):
        return "<Product(storeid='%d', itemid='%s', brandid='%d', link='%s', color='%s', title='%s', category='%s', gender='%s', uuid='%s')>" % (
                self.storeid, self.itemid, self.brandid, self.link, self.color, self.title, self.category, self.gender, self.uuid)

class ItemImage(Base):
    """"""
    __tablename__ = "itemimages"
    id = Column('id', Integer, primary_key=True)
    itemid = Column('itemid', Integer)
    imageurl = Column('imageurl', String(300))
    localurl = Column('localurl', String(300))

    def __init__(self, itemid, imageurl, localurl=None):
        self.itemid = itemid
        self.imageurl = imageurl
        self.localurl = localurl
        
    def __repr__(self):
        return "<ItemImage(itemid='%d', imageurl='%s')>" % (
                self.itemid, self.imageurl)

class ItemPrice(Base):
    """"""
    __tablename__ = "itemprices"
    id = Column('id', Integer, primary_key=True)
    itemid = Column('itemid', Integer)
    currency = Column('currency', String(10))
    checkdate = Column('checkdate', Date)
    price = Column('price', Float(255))
    
    def __init__(self, itemid, price, currency, date):
        self.itemid = itemid
        self.price = price
        self.currency = currency 
        self.checkdate = date

    def __repr__(self):
        return "<ItemPrice(itemid='%d', price='%s', currency='%s', date='%s')>" % (
                self.itemid, self.price, self.currency, self.checkdate)


class Notification(Base):
    """"""
    __tablename__ = "notifications"
    id = Column('id', Integer, primary_key=True)
    userid = Column('userid', Integer)
    message = Column('message', String(500))
    read = Column('read', Boolean)
    createdate = Column('createdate', Date)

    def __init__(self, userid, message, read, createdate):
        self.id = id
        self.userid = userid
        self.message = message
        self.read = read
        self.createdate = createdate

    def __repr__(self):
        return "<Notification(userid='%d', message='%s', read='%s', date='%s')>" % (
                self.userid, self.message, self.read, self.createdate)


class Product(Base):
    """"""
    __tablename__ = 'products'
    __table_args__ = {'autoload':True}
    id = Column('id', Integer, primary_key=True)
    storeid = Column('storeid', Integer)
    itemid = Column('itemid', String(50))
    brand = Column('brand', String(50))
    link = Column('link', String(200))
    color = Column('color', String(50))
    title = Column('title', String(200))
    category = Column('category', String(200))
    uuid = Column('uuid', String(50))
    
    def __init__(self, storeid, itemid, brand, link, color, title, category):
        self.storeid = storeid
        self.itemid = itemid
        self.brand = brand
        self.link = link
        self.color = color
        self.title = title
        self.category = category
        
    def __repr__(self):
        return "<Product(storeid='%d', itemid='%s', brand='%s', link='%s', color='%s', title='%s', category='%s', uuid='%s')>" % (
                self.storeid, self.itemid, self.brand, self.link, self.color, self.title, self.category, self.uuid)
                
class ProductImage(Base):
    """"""
    __tablename__ = "productimages"
    id = Column('id', Integer, primary_key=True)
    productid = Column('productid', Integer)
    imageurl = Column('imageurl', String(300))
    localurl = Column('localurl', String(300))

    def __init__(self, productid, imageurl):
        self.productid = productid
        self.imageurl = imageurl
        self.localurl = localurl
        
    def __repr__(self):
        return "<ProductImage(productid='%d', imageurl='%s')>" % (
                self.productid, self.imageurl)

class ProductPrice(Base):
    """"""
    __tablename__ = "productprices"
    id = Column('id', Integer, primary_key=True)
    productid = Column('productid', Integer)
    currency = Column('currency', String(10))
    checkdate = Column('checkdate', Date)
    price = Column('price', Float(255))
    

    def __init__(self, productid, price, currency, date):
        self.productid = productid
        self.price = price
        self.currency = currency 
        self.checkdate = date

    def __repr__(self):
        return "<ProductPrice(productid='%d', price='%s', currency='%s', date='%s')>" % (
                self.productid, self.price, self.currency, self.checkdate)

class Outfit(Base):
    """"""
    __tablename__ = "outfits"
    id = Column('id', Integer, primary_key=True)
    description = Column('description', String(200))
    userid = Column('userid', Integer)
    uuid = Column('uuid', String(50))

    def __init__(self, description, userid):
        self.description = description
        self.userid = userid

    def __repr__(self):
        return "<Outfit(outfitid='%d', description='%s', userid='%s')>" % (
                self.id, self.description, self.userid)

class OutfitProduct(Base):
    """"""
    __tablename__ = "outfitproducts"
    id = Column('id', Integer, primary_key=True)
    productid = Column('productid', Integer)
    outfitid = Column('outfitid', Integer)

    def __init__(self, productid, price, date):
        self.outfitid = outfitid
        self.productid = productid

    def __repr__(self):
        return "<OutfitProduct(outfitid='%d', productid='%s')>" % (
                self.outfitid, self.productid)

class Store(Base):
    """"""
    __tablename__ = 'stores'
    __table_args__ = {'autoload':True}
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(50))
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Store(name='%s')>" % (
                self.name)

class StoreBrand(Base):
    """"""
    __tablename__ = "storebrands"
    __table_args__ = {'autoload':True}
    id = Column('id', Integer, primary_key=True)
    key = Column('key', String(50))
    storeid = Column('storeid', Integer)
    brandid = Column('brandid', Integer)
    gender = Column('gender', String(10))
    url = Column('url', String(200))

    def __init__(self, key, storeid, brandid, gender, url):
        self.key = key
        self.storeid = storeid
        self.brandid = brandid
        self.gender = gender
        self.url = url

    def __repr__(self):
        return "<StoreBrand(storeid='%d', key='%s', brandid='%d'. url='%s', gender='%s')>" % (
                self.storeid, self.key, self.brandid, self.url, self.gender)

class User(Base):
    """"""
    __tablename__ = 'users'
    __table_args__ = {'autoload':True}
    id = Column('id', Integer, primary_key=True)
    name = Column('username', String(50))

class UserProduct(Base):
    """"""
    __tablename__ = "userproducts"
    id = Column('id', Integer, primary_key=True)
    userid = Column('userid', Integer)
    productid = Column('productid', Integer)

    def __init__(self, userid, productid):
        self.userid = userid
        self.productid = productid

    def __repr__(self):
        return "<UserProduct(userid='%d', productid='%d')>" % (
                self.userid, self.productid)

class Wishlist(Base):
    """" Model of the wishlists table """
    __tablename__ = 'wishlists'
    __table_args__ = {'autoload':True}
    id = Column('id', Integer, primary_key=True)
    description = Column('description', String(200))
    userid = Column('userid', Integer)
    uuid = Column('uuid', String(50))

    def __init__(self, productid, price, date):
        self.id = id

    def __repr__(self):
        return "<Wishlist(wishlistid='%d', description='%s', userid='%d', uuid='%s')>" % (
                self.id, self.description, self.userid, self.uuid)
