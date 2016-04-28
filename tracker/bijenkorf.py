################################################################################
# Application:      Outfitter
# File:             bijenkorf.py
# Goal:             
# Input:            
# Output:           
# Example:          
#
# History:          2016-02-25 - JJ     Creation of the file
#                   2016-04-19 - JJ     Refactor
#
################################################################################

################################################################################
# Imports
################################################################################
from tracker import Tracker
import orm, olog
import json
import logging
import lxml.html
import re, time
import shortuuid
import urllib2
import lxml.etree
import unidecode
import sys
from datetime import datetime

from pyvirtualdisplay import Display
from selenium import webdriver

################################################################################
# Definitions
################################################################################
__author__ = "Jitse-Jan van Waterschoot"
__copyright__ = "Copyright 2015-2016"
__credits__ = ["JItse-Jan van Waterschoot"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jitse-Jan van Waterschoot"
__email__ = "mail@jitsejan.nl"
__status__ = "Production"
HEADER = {'Accept-Language': 'nl-NL',
       'User-Agent': """Mozilla/5.0 (Windows; U;
                                    Windows NT 6.1;
                                    nl-NL;
                                    rv:1.9.1.5)
                       Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729);
                       nl-NL"""}
NUM_ITEMS = 0
################################################################################
# Functions
################################################################################

################################################################################
# Classes
################################################################################

class BijenkorfTracker(Tracker):
    """ Defines the BijenkorfTracker class """
    def __init__(self, *args, **kwargs):
        """ Initialize the BijenkorfTracker """
        super(BijenkorfTracker,self).__init__('Bijenkorf', *args, **kwargs)

    def _set_brands(self, session, insert):
        """ Sets the brands for the tracker """
        logger = logging.getLogger('outfitter')
        brands = []
        urls = {}
        urls['female'] = "http://www.debijenkorf.nl/merken/damesmode"
        urls['male']  = "http://www.debijenkorf.nl/merken/herenmode"
        for index, gender in enumerate(urls):
            logger.debug(">> Calling "+urls[gender])
            req = urllib2.Request(urls[gender], headers=HEADER)
            data = urllib2.urlopen(req).read()
            tree = lxml.html.fromstring(data)
            target = 'div[class*=\"brands-block-list\"] ul[class*=\"col\"] li a'
            brand_data = tree.cssselect(target)
            for html_data in brand_data:
                brand = self._get_brand_data(html_data)
                if brand is not False:
                    brand['gender'] = gender
                    orm_brand = self._insert_brand(session,
                                               brand,
                                               insert)
                    brands.append(orm_brand)
                else:
                    logger.error("Error retrieving brand data")
            # endfor html_data
        # endfor enumerate(urls)
        logger.info("< Found "+str(len(brands))+ " brands")
        return brands

    def _get_brand_data(self, html_data):
        """ Retrieves brand info from HTML data """
        logger = logging.getLogger('outfitter')
        brand = {}
        brand['key'] = None
        brand['name'] = None
        brand['logoUrl'] = None
        brand['logoLargeUrl'] = None
        brand['shopUrl'] = None
        burl = 'http://www.debijenkorf.nl'+html_data.attrib['href']
        logger.debug(">>> Calling "+burl)
        breq = urllib2.Request(burl, headers=HEADER)
        try:
            bdata = urllib2.urlopen(breq).read()
            btree = lxml.html.fromstring(bdata)             
            brand['name'] = self._encode_string(html_data.text_content().title())
            try: # More than 24 items per page
                atarget = 'a[class*=\"dbk-productlist-summary--link\"]'
                br_data = btree.cssselect(atarget)
                brand['shopUrl'] = br_data[1].attrib['data-href']
            except: # Less than 24 items for this brand
                brand['shopUrl'] = burl
            return brand
        except:
            return False
        
    def _get_items_for_brand(self, brand, session, insert, thisweekonly=False):
        """ Returns the items for a specific brand """
        logger = logging.getLogger('outfitter')
        items = []
        logger.debug(">>> Get articles "+brand.url)
        if thisweekonly is True:
            brand.url += '%7d%2fnieuw_nonfashion%3E%7bnet20binnen'
        try:
            req = urllib2.Request(brand.url, headers=HEADER)
            data = urllib2.urlopen(req).read()
            tree = lxml.html.fromstring(data)
        except:
            return False
        sel = 'li[class*=\"dbk-productlist-thumbnail\"] a[itemprop*=\"url\"]'
        items_data = tree.cssselect(sel)
        for article in items_data:
            if article is not None:
                itemid = article.attrib['href'].split('-')[-1]
                item = self._get_item(itemid)
                if item is None:
                    url = article.attrib['href']
                    item_data = self._get_item_data(url)
                    item = self._insert_item(session, item_data, insert)
                else:
                    logger.warning("<<<< "+str(item)+" found in DB")
                items.append(item)
                sys.exit()

        # Find pagination
        pagesel = 'ul[class*=\"dbk-pagination\"] li a'
        pagination_data = tree.cssselect(pagesel)
        if len(pagination_data) > 1:
            for page in pagination_data[1:-1]:
                sreq = urllib2.Request(page.attrib['data-href'], headers=HEADER)
                sdata = urllib2.urlopen(sreq).read()
                stree = lxml.html.fromstring(sdata)
                logger.debug(">>> Get articles for page "+page.attrib['data-href'])
                items_data = stree.cssselect('li[class*=\"dbk-productlist-thumbnail\"] a[itemprop*=\"url\"]')
                for article in items_data:
                    if article is not None:
                        url = article.attrib['href']
                        itemid = url.split('-')[-1]
                        item = self._get_item(itemid)
                        if item is None:
                            item_data = self._get_item_data(url)
                            item = self._insert_item(session,
                                                     item_data,
                                                     insert)
                        else:
                            logger.warning("<<<< "+str(item)+" found in DB")
                        items.append(item)    

        # except:
            # logger.error("<<< Opening URL failed")    
        return NUM_ITEMS
        
    def _get_item_data(self, url):
        """ Gets the item for a given ... """
        logger = logging.getLogger('outfitter')
        item = {}
        item['storeid'] = self.storeid
        if 'debijenkorf.nl' not in url:
            url = 'http://debijenkorf.nl'+url
        item['link'] = url
        item['itemid'] = item['link'].split('-')[-1]
        item['uuid'] = str(shortuuid.uuid(item['link']))
        logger.debug(">>>> "+item['link'])
        req = urllib2.Request(item['link'], headers=HEADER)
        idata = urllib2.urlopen(req).read()
        itree = lxml.html.fromstring(idata)
        brandname = self._get_brandname(idata)
        item['brandid'] = self._get_brand_id(brandname)
        item['gender'] = self._get_gender(idata)
        item['images'] = self._get_images(itree)
        item['price'] = self._get_price(idata)
        item['currency'] = self._get_currency(itree)
        item['color'] = self._get_color(itree)
        item['title'] = self._get_title(idata)
        item['category'] = self._get_category(idata)
        return item
    
    def _get_images(self, itree):
        """ Returns the images """
        images = []
        try:
            selector = 'img[data-dbk-target-selector*=\"main-image\"]'
            image_data = itree.cssselect(selector)
            for image in image_data:
                try:
                    images.append(image.attrib['data-dbk-target-src'])
                except:
                    pass # false positive
            # Return the links to the images
            if len(images) < 1:
                try:
                    src = itree.cssselect('img[class*=\"main-image\"]')[0]
                    images.append(src.attrib['src'])
                except:
                    pass
        except:
            pass
        return images

    def _get_price(self, idata):
        """ Returns the price """
        try:
            return re.search('"price": "(.*)?"', idata).group(1)
        except:
            return ""

    def _get_currency(self, itree):
        """ Returns the currency """
        try:
            currency = itree.cssselect('meta[itemprop*=\'priceCurrency\']'[0])
            return currency.attrib['content']
        except:
            return ""

    def _get_color(self, itree):
        """ Returns the color """
        try:
            color = itree.cssselect('span[itemprop*=\'color\']')[0]
            return self._encode_string(color.text_content())
        except:
            return ""

    def _get_title(self, idata):
        """ Returns the title """
        try:
            regexp = '"name": "(.*)?"'
            result = re.search(regexp, idata)
            return self._encode_string(result.group(1))
        except:
            return ""
    
    def _get_category(self, idata):
        """ Returns the category """
        try:
            result = re.search('"category": "(.*)?"', idata).group(1)
            return result.split('/')[-1]
        except:
            return ""      

    def _get_brandname(self, idata):
        """ Returns the brand """
        try:
            result = re.search('"brand": "(.*)?"', idata).group(1)
            return result
        except:
            return ""      
    
    def _get_gender(self, idata):
        """ Returns the gender """
        try:
            result = re.search('"breadcrumb" : "(.*)?"', idata).group(1)
            if 'Dames' in result:
                return 'Female'
            elif 'Heren' in result:
                return 'Male'
            else:
                return ""
        except:
            return ""      

    def _get_item_id(self, link):
        """ Get the item ID for a given Bijenkorf link """
        if 'http://' not in link:
            link = 'http://'+link
        req = urllib2.Request(link, headers=HEADER)
        data = urllib2.urlopen(req).read()
        regexp = '"masterSku" : "(.*?)",'
        result = re.search(regexp, data)
        if result:
            return result.group(1)
        else:
            return False
