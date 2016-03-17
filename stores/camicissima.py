# -*- coding: utf-8 -*-
################################################################################
# Application:      Outfitter
# File:             sephora.py
# Goal:             sephora.py will retrieve specific information from a 
#                   given Clarks link and save the data to a variable
# Input:            url of website
# Output:           Clarks Product
# Example:          newProduct() = camicissima.get_product("http://www.camicissima.com/en/shirts/shop-by-fit/extra-slim-fit/check-cotton-shirt-4.html?options=17556")
#
# History:          2015-11-02 - JJ     Creation of the file
#
################################################################################

################################################################################
# Imports
################################################################################
from product import Product
import re
import urllib2

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

class CamicissimaProduct(Product):

    def __init__(self, *args, **kwargs):
        super(CamicissimaProduct,self).__init__('Camicissima', *args, **kwargs)
        
    def _get_images(self):
        images = []
        prodid = re.search('(C[\w\d]{8}[0-9]{6})_([\w]*?)_', self._data).group(1)
        result = re.search(r'<img.*?src=\"(.*?'+prodid+'.*?)\".*?>', self._data).group(1)
        image = 'http://img01.zerogrey.com/'+result
        try:
            resp = urllib2.urlopen(urllib2.Request(image))
            images.append(image)
        except:
            pass
        
        for i in range(1,10):
            image = image.replace('img02', 'img01')
            for j in range(1,3):
                try:
                    resp = urllib2.urlopen(urllib2.Request(image.replace('_view', '_0'+str(i)+'_view')))
                    images.append(image.replace('_view', '_0'+str(i)+'_view'))
                    break
                except:
                    pass
                image = image.replace('img01', 'img02')
                
            
        return images
        
    def _get_price(self):
        try:
            return re.search('var zx_amount = "(.*)?"', self._data).group(1)
        except:
            return ""
    
    def _get_currency(self):
        try:
            price = re.search('var zx_price ="(.*)?"', self._data).group(1)
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
            return re.search('C[\w\d]{8}[0-9]{6}_([\w]*?)_', self._data).group(1).title()
        except:
            return ""
            
    def _get_title(self):
        try:
            return re.search('var zx_fn = "(.*)?"', self._data).group(1).title()
        except:
            return ""
    
    def _get_category(self):    
        try:
            return re.search('var categories = "(.*)?"', self._data).group(1).split('/')[-1]
        except:
            return ""      
   
    def _get_brand(self):
        return "Camicissima"
    
################################################################################
# main
################################################################################
def get_product(url):
    product = CamicissimaProduct(url)
    return product