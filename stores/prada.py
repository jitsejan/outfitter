# -*- coding: utf-8 -*-
################################################################################
# Application:      Outfitter
# File:             prada.py
# Goal:             prada.py will retrieve specific information from a 
#                   given Prada link and save the data to a variable
# Input:            url of website
# Output:           Prada Product
# Example:          newProduct = prada.get_product("http://www.prada.com/en/NL/e-store/man/bags/backpacks/product/2VZ135_2EUR_F0RX1_V_OOO.html")
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

class PradaProduct(Product):

    def __init__(self, *args, **kwargs):
        super(PradaProduct,self).__init__('Prada', *args, **kwargs)
        
    def _get_images(self):
        images = []
        try:
            image_data = self._tree.cssselect('li[class*=\"other-view-item\"] a img')
            for image in image_data:
                try:
                    images.append("http://www.prada.com" + image.attrib['src'])
                except:
                    pass # false positive
        except:
            pass
        return images
        
    def _get_price(self):
        try:
            return self._tree.cssselect('div[class*=\"product\"] div[class*=\"container\"] div[class*=\"right-content\"] div[class*=\"right-wrapper\"] div[class*=\"shop-content\"] div[class*=\"price\"] span')[1].text_content()[2:].replace(',', '')
        except:
            return ""
    
    def _get_currency(self):
        try:
            price = self._tree.cssselect('div[class*=\"product\"] div[class*=\"container\"] div[class*=\"right-content\"] div[class*=\"right-wrapper\"] div[class*=\"shop-content\"] div[class*=\"price\"] span')[1].text_content()[:1]
            
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
            return self._tree.cssselect('input[name*=\'item_colour\']')[0].attrib['value'].title()
        except:
            return ""
            
    def _get_title(self):
        try:
            return self._tree.cssselect('span[class*=\'nameProduct\']')[0].text_content().title()
        except:
            return ""
    
    def _get_category(self):    
        try:
            return re.search('var categories = "(.*)?"', self._data).group(1).split('/')[-1]
        except:
            return ""      
   
    def _get_brand(self):
        return "Prada"
        
################################################################################
# main
################################################################################
def get_product(url):
    product = PradaProduct(url)
    return product
    
