#!/usr/bin/env python
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = create_engine('mysql://outfitter:6qufMLA2BxmXeqe8@localhost/outfitter', echo=False)
Base = declarative_base(db)

def loadSession():
    """ Load the session """
    metadata = Base.metadata
    Session = sessionmaker(bind=db)
    session = Session()
    return session

class Brand(Base):
    """ Database model of Brand """
    __tablename__ = 'brands'
    __table_args__ = {'autoload':True}
    index = Column('id', Integer, primary_key=True)
    name = Column('name', String(150))
    logourl = Column('logourl', String(200), nullable=True)
    logolargeurl = Column('logolargeurl', String(200), nullable=True)
    uuid = Column('uuid', String(50))

    def __init__(self, **kwargs):
        valid_keys = ["name", "logourl", "logolargeurl",
                      "index", "uuid"]
        for key in valid_keys:
            self.__dict__[key] = kwargs.get(key)
        #self.name = unicode(self.name)

    def __repr__(self):
        return """<Brand(id='%s', name='%s')>""" % (self.index, self.name)

    def insert(self):
        print "Inserting", self

class Item(Base):
    """ Database model of Item """
    __tablename__ = 'items'
    __table_args__ = {'autoload':True}
    index = Column('id', Integer, primary_key=True)
    storeid = Column('storeid', Integer)
    itemid = Column('itemid', String(50))
    brandid = Column('brandid', Integer)
    link = Column('link', String(300))
    color = Column('color', String(50))
    title = Column('title', String(200))
    category = Column('category', String(200))
    gender = Column('gender', String(20))
    uuid = Column('uuid', String(50))

    def __init__(self, **kwargs):
        valid_keys = ["storeid", "itemid", "brandid",
                      "link", "color", "title",
                      "category", "gender", "uuid"]
        for key in valid_keys:
            self.__dict__[key] = kwargs.get(key)

    def __repr__(self):
        return self.title + " [" +self.link+ "]"

    def _get_brand(self, brandid):
        """ Get the brand for a given brandid """
        session = loadSession()
        orm_brand = session.query(Brand)\
                           .filter_by(index=brandid)\
                           .first()
        session.close()
        return orm_brand.name

    def _get_store(self, storeid):
        """ Get the store for a given storedid """
        session = loadSession()
        orm_store = session.query(Store)\
                           .filter_by(index=storeid)\
                           .first()
        session.close()
        return orm_store.name

    def _get_images(self):
        """ Get the images for a given item """
        session = loadSession()
        orm_images = session.query(ItemImage)\
                           .filter_by(itemid=self.index)\
                           .all()
        if len(orm_images) < 1:
            return False
        session.close()
        image_json = "["
        for image in orm_images:
            image_json += "{'url': \""+image.imageurl+"\"}, \r\n"
        image_json += "]"
        return image_json

    def _get_price(self):
        """ Get the price for a given item """
        session = loadSession()
        orm_price = session.query(ItemPrice)\
                           .filter_by(itemid=self.index)\
                           .order_by("checkdate desc")\
                           .first()
        session.close()
        return orm_price

    def __str__(self):
        return """
        Item.create({ title: '%s',
                      content:
                      {
                          itemid: '%s',
                          link: '%s',
                          color: '%s',
                          category: '%s',
                          gender: '%s',
                          brand: '%s',
                          store: '%s',
                      }
        })

        """ % (self.title, \
               self.itemid,
               self.link,
               self.color,
               self.category,
               self.gender,
               self._get_brand(self.brandid),
               self._get_store(self.storeid))

    def _to_json(self):
        images = self._get_images()
        if images:
            return """
            Item.create({ title: "%s",
                          content:
                          {
                              itemid: "%s",
                              link: "%s",
                              color: "%s",
                              category: "%s",
                              gender: "%s",
                              brand: "%s",
                              store: "%s",
                              price: "%s",
                              images: %s,
                          }
            })
    
            """ % (self.title, \
                   self.itemid,
                   self.link,
                   self.color,
                   self.category,
                   self.gender,
                   self._get_brand(self.brandid),
                   self._get_store(self.storeid),
                   self._get_price(),
                   images)

class ItemImage(Base):
    """ Database model of ItemImage """
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
    """ Database model of ItemPrice """
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
       return "<ItemPrice(itemid='%d', price='%s %s', date='%s')>" % (
                self.itemid, self.price, self.currency, self.checkdate)

class Notification(Base):
    """ Database model of Notification """
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
        return """
                <Notification(userid='%d', message='%s', read='%s', date='%s')>
               """ % (self.userid, self.message, self.read, self.createdate)


class Product(Base):
    """ Database model of Product """
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
    """ Database model of ProductImage """
    __tablename__ = "productimages"
    id = Column('id', Integer, primary_key=True)
    productid = Column('productid', Integer)
    imageurl = Column('imageurl', String(300))
    localurl = Column('localurl', String(300))

    def __init__(self, productid, imageurl, localurl=None):
        self.productid = productid
        self.imageurl = imageurl
        self.localurl = localurl

    def __repr__(self):
        return "<ProductImage(productid='%d', imageurl='%s')>" % (
                self.productid, self.imageurl)

class ProductPrice(Base):
    """ Database model of ProductPrice """
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
    """ Database model of Outfit """
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
    """ Database model of OutfitProduct """
    __tablename__ = "outfitproducts"
    id = Column('id', Integer, primary_key=True)
    productid = Column('productid', Integer)
    outfitid = Column('outfitid', Integer)

    def __init__(self, outfitid, productid):
        self.outfitid = outfitid
        self.productid = productid

    def __repr__(self):
        return "<OutfitProduct(outfitid='%d', productid='%s')>" % (
                self.outfitid, self.productid)

class Store(Base):
    """ Database model of Store """
    __tablename__ = 'stores'
    __table_args__ = {'autoload':True}
    index = Column('id', Integer, primary_key=True)
    name = Column('name', String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Store(name='%s')>" % (
                self.name)

class StoreBrand(Base):
    """ Database model of StoreBrand """
    __tablename__ = "storebrands"
    __table_args__ = {'autoload': True}
    index = Column('id', Integer, primary_key=True)
    key = Column('key', String(50))
    storeid = Column('storeid', Integer)
    brandid = Column('brandid', Integer)
    gender = Column('gender', String(10))
    url = Column('url', String(200))

    def __init__(self, key, storeid, brandid, gender, url, uuid):
        self.key = key
        self.storeid = storeid
        self.brandid = brandid
        self.gender = gender
        self.url = url
        self.uuid = uuid

    def __repr__(self):
        return "<StoreBrand(storeid='%d', key='%s', brandid='%d'. url='%s')>" % (
                self.storeid, self.key, self.brandid, self.url)

class User(Base):
    """ Database model of User """
    __tablename__ = 'users'
    __table_args__ = {'autoload':True}
    id = Column('id', Integer, primary_key=True)
    name = Column('username', String(50))

    def __init__(self, name):
        self.name = name

class UserProduct(Base):
    """ Database model of UserProduct """
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
    """" Database model of Wishlist """
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
