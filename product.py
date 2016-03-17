################################################################################
# Application:      Outfitter
# File:             product.py
# Goal:             
# Input:            
# Output:           
# Example:          
#
# History:          2015-09-24 - JJ     Creation of the file
#
################################################################################

################################################################################
# Imports
################################################################################
import urllib2 		# used to open and handle the URL
import lxml.html 	# used to convert HTML data in XML tree
import time
import shortuuid
import orm

from pyvirtualdisplay import Display
from selenium import webdriver

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

class Product(object):

    def __init__(self, store, link):
        self._store = store
        self._storeid = None
        self._brand = None
        self._link  = link
        self._images = None
        self._price = None
        self._currency = None
        self._color = None
        self._title = None
        self._category = None
        self._uuid = str(shortuuid.uuid(link))
        self._set_data()
        
    def _set_data(self):
        try:
        	if(self.get_data_from_url()):
				self._data = self.get_data_from_url()
				self._tree = self.get_tree_from_data()
				self._storeid = self.get_storeid()
				self._brand = self._get_brand()
				self._price = self._get_price()
				self._currency = self._get_currency()
				self._images = self._get_images()
				self._color = self._get_color()
				self._title = self._get_title()
				self._category = self._get_category()
        except ValueError:
            print "Could not get data"
    
    def __repr__(self):
        return "Product()" 
        
    def __str__(self):
        return '; '.join(['uuid=>'+self._uuid, 'storeid=>'+str(self._storeid), 'brand=>'+self._brand, 'link=>'+self._link, 'price=>'+self._price, 'currency=>'+self._currency, 'color=>'+self._color, 'title=>'+self._title, 'category=>'+self._category, '; '.join(self._images)])
    
    def to_csv(self):
        return '; '.join(['uuid=>'+self._uuid, 'storeid=>'+str(self._storeid), 'brand=>'+self._brand, 'link=>'+self._link, 'price=>'+self._price, 'currency=>'+self._currency, 'color=>'+self._color, 'title=>'+self._title, 'category=>'+self._category, '; '.join(self._images)])
    
    def _get_brand(self):
    	raise NotImplementedError
    	
    def _get_images(self):
        raise NotImplementedError
        
    def _get_price(self):
        raise NotImplementedError
   
    def _get_currency(self):
        raise NotImplementedError
        
    def _get_color(self):
        raise NotImplementedError
    
    def _get_title(self):
        raise NotImplementedError
    
    def _get_category(self):
        raise NotImplementedError
    
    @property
    def store(self):
        return self._store
    
    @property
    def storeid(self):
        return self._storeid
        
    @property
    def brand(self):
    	return self._brand    
    @property
    def link(self):
        return self._link
        
    @property
    def images(self):
        return self._images
        
    @property
    def price(self):
        return self._price
    
    @property
    def currency(self):
        return self._currency
        
    @property
    def color(self):
        return self._color
    
    @property
    def title(self):
        return self._title
    
    @property
    def category(self):
        return self._category
    
    def get_storeid(self):
        session = orm.loadSession()
        for result in session.query(orm.Store).filter(orm.Store.name == self._store).limit(1):
            storeid = result.id
        return storeid
    
    def get_data_from_url(self):
        data = ""
        # 1. Open the page of the URL
        # 2. Save the page to a variable
        #    urllib retrieves the HTML-data from a given link
        try:
            hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; nl-NL; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729); nl-NL'}
            
            if self._store in ['Prada', 'Camicissima']:
                display = Display(visible=0, size=(800, 600))
                display.start()
                browser = webdriver.Firefox()
                browser.get(self.link)
                data = browser.page_source
                browser.quit()
                display.stop()
            else:
                hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; nl-NL; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729); nl-NL'}
                req = urllib2.Request(self.link, headers=hdr)
                data = urllib2.urlopen(req)
                time.sleep(0)
                data = data.read()
        except:
            pass # URL broken
        # 3. Return the data as tree if successful
        if data:
            return data
        else:
            return False
	
	
    def get_tree_from_data(self):
        if self._data:
            tree = lxml.html.fromstring(self._data)
            return tree
        else:
            return False
		
		