""" outfitter/tracker/zalando.py """
# -*- coding: utf-8 -*-
################################################################################
# Application:      Outfitter
# File:             zalando.py
# Goal:
# Input:
# Output:
# Example:
# Info:             https://api.zalando.com/
#                   Should support the following URLs
# https://www.zalando.nl/nudie-jeans-slim-fit-jeans-misty-grey-nu222g02v-c11.html
# https://m.zalando.nl/komono-the-winston-regal-horloge-bruin-k0052e00p-o11.html
# http://zln.do/1SpGNWz
#
# History:          2016-02-10 - JJ     Creation of the file
#                   2016-04-11 - JJ     Massive refactor for pylint
#
################################################################################

################################################################################
# Imports
################################################################################
from outfitter.tracker.tracker import Tracker
import re
import json
import logging
import urllib, urllib2

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
MAXPAGESIZE = 200
NUM_ITEMS = 0
################################################################################
# Functions
################################################################################

################################################################################
# Classes
################################################################################

class ZalandoTracker(Tracker):
    """ Defines the ZalandoTracker class """
    def __init__(self, *args, **kwargs):
        """ Initialize the ZalandoTracker """
        super(ZalandoTracker, self).__init__('Zalando', *args, **kwargs)

    def _set_brands(self, session, insert):
        """ Sets the brands for the tracker """
        logger = logging.getLogger('outfitter')
        brands = []
        brands_url = "https://api.zalando.com/brands?pageSize="+str(MAXPAGESIZE)
        logger.info("> Calling "+brands_url)
        req = urllib2.Request(brands_url, headers=HEADER)
        brands_json = json.loads(urllib2.urlopen(req).read())
        total_elements = brands_json['totalElements']
        if total_elements > 0:
            for page in range(brands_json['totalPages']):
                brand_url = brands_url+"&page="+str(page+1)
                logger.debug(">> Calling "+brand_url)
                brand_json = json.loads(urllib.urlopen(brand_url).read())
                for json_b in brand_json['content']:
                    brand = self._get_brand_data(json_b)
                    orm_brand = self._insert_brand(session,
                                                   brand,
                                                   insert)
                    brands.append(orm_brand)
                # endfor json_b
            # endfor page
        # endfor total_elements
        logger.info("< Found "+str(len(brands))+ " brands")
        return brands

    def _get_brand_data(self, json_data):
        """ Retrieves brand info from json data """
        logger = logging.getLogger('outfitter')
        brand = {}
        brand['key'] = None
        brand['name'] = None
        brand['logoUrl'] = None
        brand['logoLargeUrl'] = None
        brand['gender'] = None
        brand.update(json_data)
        brand['name'] = self._encode_string(brand['name'])
        return brand

    def _get_items_for_brand(self, brand, session, insert, thisweekonly=False):
        """ Returns the items for a specific brand """
        logger = logging.getLogger('outfitter')
        items = []
        articles_url = "https://api.zalando.com/articles"
        articles_url += "?pageSize="+str(MAXPAGESIZE)
        articles_url += "&brand=" + str(brand.key)
        if thisweekonly is True:
            articles_url += '&activationDate=thisWeek'
        logger.debug(">>> Get articles "+articles_url)
        req = urllib2.Request(articles_url, headers=HEADER)
        try:
            articles_json = json.loads(urllib2.urlopen(req).read())
        except:
            return False
        total_elements = articles_json['totalElements']
        logger.debug("<<< Number of items "+ str(total_elements))
        if total_elements > 0:
            for page in range(articles_json['totalPages']):
                article_url = articles_url+"&page="+str(page+1)+"&fields=id"
                logger.debug(">>>> Get articles per page " + article_url)
                article_jsn = json.loads(urllib.urlopen(article_url).read())
                if 'content' in article_jsn.keys():
                    for article in article_jsn['content']:
                        if article is not None:
                            item = self._get_item(article['id'])
                            if item is None:
                                item_data = self._get_item_data(link=None, itemid=article['id'])
                                item = self._insert_item(session,
                                                         item_data,
                                                         insert)
                            else:
                                logger.warning("<<<< "+str(item)+" found in DB")
                            items.append(item)
                        #endif article is not None
                    #endfor it in articleJson['content']
                else:
                    logger.error("<<< JSON data invalid")
                #endif content in keys
            #endfor for page in range(pages)
        #endif for totalElements > 0
        # except:
            # logger.error("<<< Opening URL failed")
        logger.debug("<<< Found "+str(NUM_ITEMS)+" items")
        return items

    def _get_item_data(self, link, itemid=None):
        """ Gets the item for a given link """
        logger = logging.getLogger('outfitter')
        if link is not None:
            itemid = self._get_item_id(link)
        item_url = "https://api.zalando.com/articles?articleID="+itemid
        logger.debug(">>>> "+item_url)
        req = urllib2.Request(item_url, headers=HEADER)
        page_json = json.loads(urllib2.urlopen(req).read())
        if 'content' in page_json.keys():
            if len(page_json['content']) > 0:
                item_json = page_json['content'][0]
            else:
                return False
        else:
            return False
        try:
            item = {}
            item['storeid'] = self.storeid
            brandname = item_json['brand']['name']
            item['brandid'] = self._get_brand_id(brandname)
            item['itemid'] = item_json['id']
            item['title'] = self._encode_string(item_json['name'])
            item['link'] = item_json['shopUrl']
            item['color'] = item_json['color']
            item['category'] = item_json['categoryKeys'][4]
            item['price'] = item_json['units'][0]['price']['value']
            item['currency'] = item_json['units'][0]['price']['currency']
            item['gender'] = ', '.join(item_json['genders']).title()
            item['uuid'] = self._create_uuid(self._encode_string(item['link']))
            item['images'] = []
            for image in item_json['media']['images']:
                item['images'].append(image['largeUrl'])
            logger.debug("<<<< Retrieving data successful for "+str(itemid)+"")
            return item
        except:
            logger.error("<<<< Retrieving data failed for "+str(item_url)+"")
            return False

    def _get_item_id(self, link):
        """ Get the item ID for a given Zalando link """
        req = urllib2.Request(link, headers=HEADER)
        data = urllib2.urlopen(req).read()
        regexp = '"productSku":"(.*?)",'
        result = re.search(regexp, data)
        if result:
            return result.group(1)
        else:
            return False
    