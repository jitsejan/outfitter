################################################################################
# Application:      Outfitter
# File:             productfactory.py
# Goal:             
# Input:            
# Output:           
# Example:          
#
# History:          2015-10-07 - JJ     Creation of the file
#
################################################################################

################################################################################
# Imports
################################################################################

from stores import asos, zalando, tedbaker, zara, topshop, tommyhilfiger, clarks, camicissima, sarenza
from stores import iciparis, douglas, sephora, bijenkorf, prada, miumiu, ralphlauren

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

class ProductFactory(object):
    
    def __init__(self, url):
        self._url = url;

    @classmethod
    def create_product(self, url):
        if 'http' not in url:
            url = 'http://' + url
        if 'www.asos.com' in url:
            newProduct = asos.get_product(url)
        elif 'www.zara.com' in url:
            newProduct = zara.get_product(url)
        elif 'zalando' in url:
            newProduct = zalando.get_product(url)
        elif 'www.tedbaker.com' in url:
            newProduct = tedbaker.get_product(url)
        elif 'topman.com' in url:
            newProduct = topshop.get_product(url)
        elif 'topshop.com' in url:
            newProduct = topshop.get_product(url)
        elif 'tommy.com' in url:
            newProduct = tommyhilfiger.get_product(url)
        elif 'iciparisxl' in url:
            newProduct = iciparis.get_product(url)
        elif 'douglas' in url:
            newProduct = douglas.get_product(url)
        elif '.clarks' in url:
            newProduct = clarks.get_product(url)
        elif 'sephora' in url:
            newProduct = sephora.get_product(url)
        elif 'camicissima' in url:
            newProduct = camicissima.get_product(url)
        elif '.sarenza.' in url:
            newProduct = sarenza.get_product(url)
        elif '.debijenkorf.' in url:
            newProduct = bijenkorf.get_product(url)
        elif '.prada.com' in url:
            newProduct = prada.get_product(url)
        elif '.miumiu.com' in url:
            newProduct = miumiu.get_product(url)
        elif '.ralphlauren.' in url:
            newProduct = ralphlauren.get_product(url)
        else:
            newProduct = False

        return newProduct        