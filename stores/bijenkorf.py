# -*- coding: utf-8 -*-
################################################################################
# Application:      Outfitter
# File:             bijenkorf.py
# Goal:             bijenkorf.py will retrieve specific information from a 
#                   given Bijenkorf link and save the data to a variable
# Input:            url of website
# Output:           Bijenkorf Product
# Example:          newProduct = bijenkorf.get_product("http://www.debijenkorf.nl/maison-scotch-sweater-met-kleurrijke-emblemen-9744030020-974403002051002")
#
# History:          2016-02-18 - JJ     Creation of the file
#
################################################################################

################################################################################
# Imports
################################################################################
from product import Product
import re
import urllib2
import lxml.html

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

class BijenkorfProduct(Product):

    def __init__(self, *args, **kwargs):
        super(BijenkorfProduct,self).__init__('Bijenkorf', *args, **kwargs)
        
    def _get_images(self):
        images = []
        try:
            image_data = self._tree.cssselect('img[data-dbk-target-selector*=\"main-image\"]')
            for image in image_data:
                try:
                    images.append(image.attrib['data-dbk-target-src'])
                except:
                    pass # false positive
            # Return the links to the images
            if len(images) < 1:
                try:
                    images.append(self._tree.cssselect('img[class*=\"main-image\"]')[0].attrib['src'])
                except:
                    pass
        except:
            pass
        return images
        
    def _get_price(self):
        try:
            return self._tree.cssselect('span[itemprop*=\'price\']')[0].text_content().strip().replace(',','.')
        except:
            return ""
    
    def _get_currency(self):
        try:
            return self._tree.cssselect('meta[itemprop*=\'priceCurrency\']')[0].attrib['content']
        except:
            return "EUR"
    
    def _get_color(self):
        try:
            return self._tree.cssselect('span[itemprop*=\'color\']')[0].text_content()
        except:
            return ""
            
    def _get_title(self):
        try:
            regexp = '"name": "(.*)?"'
            result = re.search(regexp, self._data)
            return result.group(1)
        except:
            return ""
    
    def _get_category(self):    
        try:
            return re.search('"category": "(.*)?"', self._data).group(1).split('/')[-1]
        except:
            return ""      
   
    def _get_brand(self):
        try:
            return re.search('"brand": "(.*)?"', self._data).group(1)
        except:
            return ""
        
################################################################################
# main
################################################################################
def get_product(url):
    if 'm.debijenkorf' in url:
        url = get_bijenkorf_url(url)
    product = BijenkorfProduct(url)
    return product
    
def get_bijenkorf_url(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; nl-NL; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729); nl-NL'}
    req = urllib2.Request(url, headers=hdr)
    data = urllib2.urlopen(req).read()
    tree = lxml.html.fromstring(data)
    return tree.cssselect('link[rel*=\"canonical\"]')[0].attrib['href']
    
