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

################################################################################
# Imports
################################################################################
from outfitter import orm

import datetime
import re
import time
import urllib
################################################################################
# Definitions
################################################################################
author =    "JJ"
appName =   "Outfitter"

################################################################################
# Functions
################################################################################
        
################################################################################
# Classes
################################################################################

class Tracker(object):

    def __init__(self, store):
        self._store = store
        self._storeid = self._get_store_id()
        self._brands = None
        self._items = {}
        # self._set_data()
        
    def set_data(self):
        try:
            self._brands = self._get_brands()
        except ValueError:
            print "Could not get data"
    
    def __repr__(self):
        return "Tracker()" 
        
    def __str__(self):
        return '; '.join(['store=>'+self._store, 'storeid=>'+str(self._storeid)])

    def to_csv(self):
        return '; '.join(['store=>'+self._store])
    
    def _get_brands(self, session):
        storebrands = session.query(orm.StoreBrand, orm.Brand).join(orm.Brand, orm.StoreBrand.brandid == orm.Brand.id)\
                                              .filter(orm.StoreBrand.storeid == self.storeid).all()
        return storebrands
    	
    @property
    def store(self):
        return self._store
    
    @property
    def storeid(self):
        return self._storeid
        
    @property
    def brands(self):
        return self._brands
        
    def _get_store_id(self):
        session = orm.loadSession()
        for result in session.query(orm.Store).filter(orm.Store.name == self._store).limit(1):
            storeid = result.id
        return storeid
