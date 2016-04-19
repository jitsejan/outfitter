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

################################################################################
# Imports
################################################################################
from outfitter import orm

from datetime import datetime
import logging
import shortuuid
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
        self._store = store
        self._storeid = self._get_store_id()
        self._brands = None
        self._items = {}
        self._session = session
        self._set_data()

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
        for result in session.query(orm.Store)\
                .filter(orm.Store.name == self._store).limit(1):
            storeid = result.id
        return storeid

    def _get_brand_id(self, brandname):
        """ Get the ID for a given brandname """
        session = orm.loadSession()
        for result in session.query(orm.Brand)\
                .filter(orm.Brand.name == brandname).limit(1):
            brandid = result.index
        return brandid
        
    def _get_storebrand(self, brandname):
        """ Get the brand for a given brankname """
        session = orm.loadSession()
        for result in session.query(orm.StoreBrand)\
                    .join(orm.Brand, orm.StoreBrand.brandid == orm.Brand.index)\
                    .filter(orm.Brand.name == brandname)\
                    .filter(orm.StoreBrand.storeid == self.storeid)\
                    .limit(1):
            brand = result
        return brand

    def to_csv(self):
        """ Print to CSV format """
        return '; '.join(['store=>'+self._store])

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
        start = datetime.now()
        for storebrand in self._brands:
            num_items = self._get_items_for_brand(storebrand[0], session, insert=True, thisweekonly=True)
            tot_num_items += num_items
        end = datetime.now()
        logger.debug("< Added "+str(tot_num_items)+" new items in "+ str(end-start) +"!")
        
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
