""" tracker/asos.py """
# -*- coding: utf-8 -*-
################################################################################
# Application:      Outfitter
# File:             asos.py
# Goal:
# Input:
# Output:
# Example:
#
# History:          2016-02-10 - JJ     Creation of the file
#                   2016-04-21 - JJ     Refactor for Pylint
#
################################################################################

################################################################################
# Imports
################################################################################
from outfitter.tracker.tracker import Tracker
import re
import lxml.html
import urllib2
import logging

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

class AsosTracker(Tracker):
    """ Defines the AsosTracker class """
    def __init__(self, *args, **kwargs):
        """ Initialize the ZalandoTracker """
        super(AsosTracker, self).__init__('Asos', *args, **kwargs)

    def _set_brands(self, session, insert):
        """ Sets the brands for the tracker """
        logger = logging.getLogger('outfitter')
        brands = []
        urls = {}
        urls['male'] = "http://www.asos.com/men/" \
                       "a-to-z-of-brands/cat/pgehtml.aspx?cid=1361"
        urls['female'] = "http://www.asos.com/Women" \
                         "/A-To-Z-Of-Brands/Cat/pgehtml.aspx?cid=1340"
        for _, gender in enumerate(urls):
            logger.debug(">> Calling "+urls[gender])
            req = urllib2.Request(urls[gender], headers=HEADER)
            data = urllib2.urlopen(req).read()
            tree = lxml.html.fromstring(data)
            brandsel = 'div[id*=\"brands_section\"] div ul li a'
            brand_data = tree.cssselect(brandsel)
            for html_data in brand_data:
                brand = self._get_brand_data(html_data)
                brand['gender'] = gender
                orm_brand = self._insert_brand(session,
                                               brand,
                                               insert)
                brands.append(orm_brand)
             # endfor html_data
        # endfor enumerate(urls)
        logger.info("< Found "+str(len(brands))+ " brands")
        return brands

    def _get_brand_data(self, html_data):
        """ Retrieves brand info from HTML data """
        brand = {}
        brand['name'] = self._encode_string(html_data.text_content()).strip()
        brand['logoUrl'] = None
        brand['logoLargeUrl'] = None
        brand['shopUrl'] = html_data.attrib['href']
        try:
            brand['key'] = html_data.attrib['href'].rsplit('=', 1)[1]
        except:
            brand['key'] = None
        return brand

    def _get_items_for_brand(self, brand, session, insert, thisweekonly=False):
        """ Returns the items for a specific brand """
        logger = logging.getLogger('outfitter')
        items = []
        logger.debug(">>> Get articles "+brand.url)
        req = urllib2.Request(brand.url.replace(' ', '%20'), headers=HEADER)
        # try:
        data = urllib2.urlopen(req).read()
        tree = lxml.html.fromstring(data)
        # itemsel = r"div[id*=\"items-wrapper\"] ul[id*=\"items\"] li " \
        #           r"div[class*=\"categoryImageDiv\"] " \
        #           r"a[class*=\"productImageLink\"]"
        #items_data = tree.cssselect('div[id*=\"items-wrapper\"] ul[id*=\"items\"] li div[class*=\"categoryImageDiv\"] a[class*=\"productImageLink\"]')
        
        items_data = tree.cssselect('li[class*=\"product-container\"] a[class*=\"product product-link\"]')
        for article in items_data:
            if article is not None:
                itemid = article.attrib['href'].split('&')[0].split('=')[1]
                item = self._get_item(itemid)
                if item is None:
                    itemurl = article.attrib['href'].replace(' ', '%20')
                    item_data = self._get_item_data(itemurl)
                    item = self._insert_item(session, item_data, insert)
                else:
                    logger.warning("<<<< "+str(item)+" found in DB")
                items.append(item)
        # except:
            # logger.error("<<< Opening URL failed")
        return items

    def _get_item_data(self, itemurl):
        """ Gets the item for a given url """
        item = {}
        item['storeid'] = self.storeid
        item['link'] = itemurl
        item['itemid'] = item['link'].split('=')[1].split('&')[0]
        req = urllib2.Request(item['link'], headers=HEADER)
        idata = urllib2.urlopen(req).read()
        itree = lxml.html.fromstring(idata)
        item['images'] = self._get_images(itree)
        item['price'] = self._get_price(item['link'])
        item['currency'] = self._get_currency()
        item['color'] = self._get_color(itree, item['images'][0])
        item['title'] = self._get_title(itree)
        item['category'] = self._get_category(itree)
        item['gender'] = self._get_gender(itree)
        item['uuid'] = self._create_uuid(item['link'])
        brandname = self._get_brandname(itree)
        print item['link']
        print 'brandname', brandname
        item['brandid'] = self._get_brand_id(brandname)
        return item

    def _get_images(self, itree):
        """ Returns the images """
        images = []
        try:
            imagesel = 'div[id*=\"productImages\"] '\
                       'div[class*=\"productImagesItems\"] '\
                       'div[class*=\"image\"] '\
                       'img'
            image_data = itree.cssselect(imagesel)
            for image in image_data:
                if 'src' in image.attrib.keys():
                    images.append(image.attrib['src'])
        except Exception:
            pass
        return images

    def _get_price(self, url):
        """ Returns the price """
        url = url.replace('.com/', '.com/it/')
        req = urllib2.Request(url, headers=HEADER)
        idata = urllib2.urlopen(req).read()
        try:
            regexp = '"ProductPriceInNetworkCurrency":"(.*?)"'
            result = re.search(regexp, idata)
            price = result.group(1)
        except Exception:
            price = ""
        return price

    def _get_currency(self):
        """ Returns the currency """
        currency = 'EUR' # Cheat, since for the price we pick the EUR version
        return currency

    def _get_color(self, itree, image):
        """ Returns the color """
        try:
            colorsel = 'div[class*=\'colour\'] option[selected*=\'selected\']'
            color = itree.cssselect(colorsel)[0]
            if 'value' in color.attrib.keys():
                return color.attrib['value']
        except Exception:
            try:
                regexp = r"http:\/\/images.asos-media.com\/inv\/media\/[\d]*"\
                         r"\/[\d]*\/[\d]*\/[\d]*\/[\d]*\/([\w]*)\/[\d\w]*.jpg"
                result = re.search(regexp, image)
                color = result.group(1)
            except Exception:
                color = ""
        return color

    def _get_title(self, itree):
        """ Returns the title """
        try:
            titlesel = 'div[class*=\'title\'] h1'
            title = itree.cssselect(titlesel)[0].text_content().strip()
        except Exception:
            title = ""
        return self._encode_string(title)

    def _get_category(self, itree):
        """ Returns the category """
        try:
            categorysel = 'div[id*=\'ctl00_ContentMainPage_productInfoPanel\']'\
                          ' strong'
            category = itree.cssselect(categorysel)[0].text_content().strip()
        except Exception:
            category = ""
        return self._encode_string(category)

    def _get_brandname(self, itree):
        """ Returns the brand """
        try:
            brandsel = 'div[id*=\'ctl00_ContentMainPage_brandInfoPanel\'] h2'
            brand = itree.cssselect(brandsel)[0].text_content()
            print brand.split("ABOUT ")[1].title()
            return brand.split("ABOUT ")[1].title()
        except Exception:
            return False

    def _get_gender(self, itree):
        """ Returns the gender """
        try:
            breadcrumbsel = 'div[class*=\'breadcrumbs\'] a'
            breadcrumb = itree.cssselect(breadcrumbsel)
            if 'Men' in breadcrumb[-1].attrib['href']:
                return 'Male'
            if 'Women' in breadcrumb[-1].attrib['href']:
                return 'Female'
            return ""
        except:
            return ""  

    def _get_item_id(self, link):
        """ Get the item ID for a given Asos link """
        print 'Link', link
        regexp = 'iid=(.*?)&'
        result = re.search(regexp, link)
        if result:
            return result.group(1)
        else:
            return False