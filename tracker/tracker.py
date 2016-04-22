""" tracker/tracker.py """
# -*- coding: utf-8 -*-
################################################################################
# Application:      Outfitter
# File:             tracker.py
# Goal:
# Input:
# Output:
# Example:
#
# History:          2016-02-09 - JJ     Creation of the file
#                   2016-04-21 - JJ     Refactor, move functions to main class
#
################################################################################
__author__ = "Jitse-Jan van Waterschoot"
__copyright__ = "Copyright 2015-2016"
__credits__ = ["JItse-Jan van Waterschoot"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jitse-Jan van Waterschoot"
__email__ = "mail@jitsejan.nl"
__status__ = "Production"

NUM_ITEMS = 0

################################################################################
# Imports
################################################################################
from outfitter import orm

from datetime import datetime
import logging
import shortuuid
import sys
import time

################################################################################
# Definitions
################################################################################

################################################################################
# Functions
################################################################################

################################################################################
# Classes
################################################################################

class Tracker(object):
    """ Defines the Tracker class """
    def __init__(self, store, session):
        """ Initizalize the tracker """
        logger = logging.getLogger('outfitter')
        self._store = store
        self._storeid = self._get_store_id()
        self._brands = None
        self._items = {}
        self._session = session
        self._set_data()
        logger.info("> Initialize tracker "+str(self))

    def _set_data(self):
        """ Set the data for the tracker """
        try:
            self._brands = self._get_brands(self._session)
        except ValueError:
            print "Could not get data"

    def __repr__(self):
        """ Representation of the class """
        return "Tracker()"

    def __str__(self):
        """ Print to string """
        return '; '.join(['store=>'+self._store, 'id=>'+str(self._storeid)])

    @property
    def store(self):
        """ Return the store """
        return self._store

    @property
    def storeid(self):
        """ Return the storeid """
        return self._storeid

    @property
    def brands(self):
        """ Return the brands """
        return self._brands

    def _get_store_id(self):
        """ Get the ID for a given store """
        session = orm.loadSession()
        store = session.query(orm.Store)\
                .filter(orm.Store.name == self._store)\
                .limit(1)\
                .first()
        session.close()
        return store.index

    def _get_brand_id(self, brandname):
        """ Get the ID for a given brandname """
        session = orm.loadSession()
        brand = session.query(orm.Brand)\
                             .filter(orm.Brand.name == brandname)\
                             .limit(1)\
                             .first()
        session.close()
        return brand.index

    def _get_storebrand(self, brandname, gender=None):
        """ Get the storebrand for a given brandname """
        session = orm.loadSession()
        orm_storebrand = session.query(orm.StoreBrand)\
                    .join(orm.Brand, orm.StoreBrand.brandid == orm.Brand.index)\
                    .filter(orm.Brand.name == brandname)\
                    .filter(orm.StoreBrand.storeid == self.storeid)\
                    .filter(orm.StoreBrand.gender == gender)\
                    .limit(1)\
                    .first()
        session.close()
        return orm_storebrand

    def to_csv(self):
        """ Print to CSV format """
        return '; '.join(['store=>'+self._store])

    def _get_item(self, itemid):
        """ Returns item based on store and itemid """
        session = orm.loadSession()
        orm_item = session.query(orm.Item)\
                        .filter_by(itemid=itemid)\
                        .filter_by(storeid=self.storeid)\
                        .first()
        session.close()
        return orm_item

    def _get_brand(self, brandname):
        """ Get the brand for a given brandname """
        session = orm.loadSession()
        orm_brand = session.query(orm.Brand)\
                           .filter_by(name=unicode(brandname))\
                           .first()
        session.close()
        return orm_brand

    def _get_brands(self, session):
        """ Get the brands for a specific store """
        storebrands = session.query(orm.StoreBrand, orm.Brand)\
                    .join(orm.Brand, orm.StoreBrand.brandid == orm.Brand.index)\
                    .filter(orm.StoreBrand.storeid == self.storeid).all()
        return storebrands

    def _get_number_of_brands(self, session):
        """ Returns the number of brands """
        storebrands = session.query(orm.StoreBrand)\
                    .join(orm.Brand, orm.StoreBrand.brandid == orm.Brand.index)\
                    .filter(orm.StoreBrand.storeid == self.storeid).all()
        return len(storebrands)

    def _encode_string(self, string):
        """ Encode the input string and escape characters """
        return unicode(string).encode('ascii', 'xmlcharrefreplace')

    def _create_uuid(self, string):
        """ Create a UUID from input string """
        return shortuuid.uuid(string)

    def _get_new_items(self, session):
        """ Retrieves the items recently added """
        logger = logging.getLogger('outfitter')
        tot_num_items = 0
        all_items = []
        start = datetime.now()
        for storebrand in self._brands:
            items = self._get_items_for_brand(storebrand[0],
                                                  session,
                                                  insert=True,
                                                  thisweekonly=True)
            all_items.append(items)
            tot_num_items += len(items)
        end = datetime.now()
        diff = str(end-start)
        logger.debug("< Added "+str(tot_num_items)+" new items in "+ diff +"!")

    def _get_all_items(self, session):
        """ Retrieves all the items """
        logger = logging.getLogger('outfitter')
        tot_num_items = 0
        all_items = []
        start = datetime.now()
        for storebrand in self._brands:
            items = self._get_items_for_brand(storebrand[0],
                                              session,
                                              insert=True,
                                              thisweekonly=False)
            all_items.append(items)
            tot_num_items += len(items)
        end = datetime.now()
        diff = str(end-start)
        logger.debug("< Added "+str(tot_num_items)+" items in "+ diff +"!")

    def _insert_images(self, session, item, itemid, insert):
        """ Inserts the images for an item """
        logger = logging.getLogger('outfitter')
        images = []
        logger.info("<<<< Inserting images.. ")
        for imageurl in item['images']:
            image = self._insert_image(session, imageurl, itemid, insert)
            images.append(image)
        return images

    def _insert_image(self, session, imageurl, itemid, insert):
        """ Inserts an image for an item """
        logger = logging.getLogger('outfitter')
        item_image = session.query(orm.ItemImage)\
                        .filter_by(itemid=itemid)\
                        .filter_by(imageurl=imageurl)\
                        .first()
        if item_image is None:
            if insert is True:
                item_image = orm.ItemImage(itemid, imageurl)
                logger.info("<<<< Inserted image "+str(item_image))
                session.add(item_image)
                session.flush()
                session.commit()
            else:
                logger.debug("<<<< Should insert image "+str(item_image))
        else:
            logger.debug("<<<< Image "+str(item_image)+" already in database")
        return item_image

    def _insert_price(self, session, item, itemid, insert):
        """ Inserts the price for an item """
        logger = logging.getLogger('outfitter')
        shortdate = time.strftime('%Y-%m-%d')
        item_price = session.query(orm.ItemPrice)\
                            .filter_by(itemid=itemid)\
                            .filter_by(checkdate=shortdate)\
                            .first()
        if item_price is None:
            item_price = orm.ItemPrice(itemid,
                                   item['price'],
                                   item['currency'],
                                   shortdate)
            if insert is True:
                session.add(item_price)
                session.flush()
                session.commit()
                logger.info("<<<< Inserting price "+str(item_price))
            else:
                logger.debug("<<<< Should insert price "+str(item_price))
        else:
            logger.debug("<<<< Price "+str(item_price)+" already in database")
        return item_price

    def _insert_item(self, session, item, insert):
        """ Inserts an item """
        global NUM_ITEMS
        logger = logging.getLogger('outfitter')
        orm_item = self._get_item(item['itemid'])
        if orm_item is None:
            if item is not False:
                orm_item = orm.Item(storeid=item['storeid'],
                                      itemid=item['itemid'],
                                      brandid=item['brandid'],
                                      link=item['link'],
                                      color=item['color'],
                                      title=item['title'],
                                      category=item['category'],
                                      gender=item['gender'],
                                      uuid=item['uuid'])
                if insert is True:
                    session.add(orm_item)
                    session.flush()
                    session.commit()
                    itemid = orm_item.index
                    NUM_ITEMS += 1
                    logger.info("<<<< Inserted "+str(orm_item))
                    self._insert_images(session, item, itemid, insert)
                    self._insert_price(session, item, itemid, insert)
                else:
                    logger.debug("<<<< Should insert "+str(orm_item))
            #endif item is not False
        else:
            itemid = orm_item.index
            logger.debug("<<<< "+orm_item.title+" [id " + str(itemid)+"]")
        #endif i is None
        return orm_item

    def _insert_brand(self, session, brand, insert):
        """ Inserts a brand in the database if insert is True """
        logger = logging.getLogger('outfitter')
        orm_brand = self._get_brand(brand['name'])
        if orm_brand is None:
            uuid = self._create_uuid(brand['name'])
            orm_brand = orm.Brand(brand['name'],
                                  brand['logoUrl'],
                                  brand['logoLargeUrl'],
                                  uuid)
            if insert is True:
                session.add(orm_brand)
                session.flush()
                session.commit()
                logger.info("<<< Inserted brand "+str(orm_brand))
            else:
                logger.info("<<< Should insert brand "+str(orm_brand))
        else:
            brandid = orm_brand.index
            logger.debug("<<< Brand "+orm_brand.name+" [" +str(brandid)+"]")

        self._insert_storebrand(session, brand, insert)

        return orm_brand

    def _insert_storebrand(self, session, brand, insert):
        """ Inserts a storebrand in the database if insert is True """
        logger = logging.getLogger('outfitter')
        uuid = self._create_uuid(self._encode_string(brand['shopUrl']))
        orm_storebrand = self._get_storebrand(brand['name'], brand['gender'])
        if orm_storebrand is None:
            brandid = self._get_brand_id(brand['name'])
            orm_storebrand = orm.StoreBrand(key=brand['key'],
                                            storeid=self.storeid,
                                            brandid=brandid,
                                            gender=brand['gender'],
                                            url=brand['shopUrl'],
                                            uuid=uuid)
            if insert is True:
                session.add(orm_storebrand)
                session.commit()
                session.flush()
                logger.info("<<< Inserted storebrand "+str(orm_storebrand))
            else:
                logger.info("<<< Should insert storebrand "+str(orm_storebrand))
        return orm_storebrand
