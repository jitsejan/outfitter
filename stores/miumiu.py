# -*- coding: utf-8 -*-
################################################################################
# Application:      Outfitter
# File:             miumiu.py
# Goal:             miumiu.py will retrieve specific information from a 
#                   given Prada link and save the data to a variable
# Input:            url of website
# Output:           MiuMiu Product
# Example:          newProduct = miumiu.get_product("http://store.miumiu.com/en/NL/dep/accessories/cat/keyholders/product/5TL051_2E0H_F0135#department_view=true&ref=1455808822691")
#
# History:          2016-02-18 - JJ     Creation of the file
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

class MiuMiuProduct(Product):

    def __init__(self, *args, **kwargs):
        super(MiuMiuProduct,self).__init__('MiuMiu', *args, **kwargs)
        
    def _get_images(self):
        images = []
        try:
            image_data = self._tree.cssselect('ul[id*=\"views\"] li a[class*=\"product-view\"] img')
            for image in image_data:
                try:
                    images.append("http://store.miumiu.com" + image.attrib['src'].replace('views', 'details'))
                except:
                    pass # false positive
        except:
            pass
        return images
        
    def _get_price(self):
        try:
            return self._tree.cssselect('div[id*=\"item-price\"] span')[0].text_content()[1:].replace(',', '')
        except:
            return ""
    
    def _get_currency(self):
        try:
            price = self._tree.cssselect('div[id*=\"item-price\"] span')[0].text_content()[:1]
            
            if u"£" in price:
                currency = 'GBP'
            elif u"€" in price:
                currency = 'EUR'
            elif u"$" in price:
                currency = "USD"
            return currency
        except:
            return ""
    
    def _get_color(self):
        try:
            return self._tree.cssselect('li[id*=\'selected-color\']')[0].text_content().title()
        except:
            return ""
            
    def _get_title(self):
        try:
            return unicode(self._tree.cssselect('div[id*=\'detail_description\'] h2')[0].text_content().title()).encode('ascii', 'xmlcharrefreplace')
        except:
            return ""
    
    def _get_category(self):    
        try:
            return self._tree.cssselect('div[id*=\'categories\'] a[class*=\"selected\"]')[0].text_content().title()
        except:
            return ""      
   
    def _get_brand(self):
        return "MiuMiu"
        
################################################################################
# main
################################################################################
def get_product(url):
    product = MiuMiuProduct(url)
    return product
    
