# -*- coding: utf-8 -*-
################################################################################
# Application:      Outfitter
# File:             ralphlauren.py
# Goal:             ralphlauren.py will retrieve specific information from a 
#                   given Ralph Lauren link and save the data to a variable
# Input:            url of website
# Output:           Ralp Lauren Product
# Example:          newProduct = ralphlauren.get_product("http://www.ralphlauren.fr/product/index.jsp?productId=55575681")
#
# History:          2016-02-19 - JJ     Creation of the file
#
################################################################################

################################################################################
# Imports
################################################################################
from product import Product
import re

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

class RalphLaurenProduct(Product):

    def __init__(self, *args, **kwargs):
        super(RalphLaurenProduct,self).__init__('Ralph Lauren', *args, **kwargs)
        
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
        except:
            pass
        return images
        
    def _get_price(self):
        try:
            return re.search('"price": "(.*)?"', self._data).group(1)
        except:
            return ""
    
    def _get_currency(self):
        try:
            return self._tree.cssselect('meta[itemprop*=\'priceCurrency\']')[0].attrib['content']
        except:
            return ""
    
    def _get_color(self):
        try:
            return self._tree.cssselect('span[itemprop*=\'color\']')[0].text_content()
        except:
            return ""
            
    def _get_title(self):
        print 'LOL'
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
    product = RalphLaurenProduct(url)
    return product
    
