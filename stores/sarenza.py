# -*- coding: utf-8 -*-
################################################################################
# Application:      Outfitter
# File:             sarenza.py
# Goal:             sarenza.py will retrieve specific information from a 
#                   given Sarenza link and save the data to a variable
# Input:            url of website
# Output:           Sarenza Product
# Example:          newProduct() = sarenza.get_product("http://www.sarenza.nl/ted-baker-tephra-2-s1455-p0000048390")
#
# History:          2016-02-09 - JJ     Creation of the file
#
################################################################################

################################################################################
# Imports
################################################################################
from product import Product
import re
from unidecode import unidecode
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

class SarenzaProduct(Product):

    def __init__(self, *args, **kwargs):
        super(SarenzaProduct,self).__init__('Sarenza', *args, **kwargs)
        
    ################################################################################
    # Function:         _get_image
    # Input:            tree
    # Output:           URL of the image
    # Goal:             Find the image URL and return it
    # Targets:          Use a css selecter to find the image URL
    # Example:          <div class="product-view"><div class='product-gallery'><div class='iosSlider'><div class='slider'><div class='slide'><img src="http://cdn3.sarenza.net/static/_img/productsV4/0000048390/MD_0000048390_81885_09.jpg?201308210332" itemprop="image" alt="Ted Baker Mocassins TEPHRA 2 3/4'" />
    def _get_images(self):
        images = []
        try:
            # Use css to select image
            image_data = self._tree.cssselect('div[class*=\"product-view\"] div[class*=\"product-gallery\"] div[class*=\"iosSlider\"] div[class*=\"slider\"] div[class*=\"slide\"] img[itemprop*=\"image\"]')
            for image in image_data:
                image_link = image.attrib['src']
                images.append(image_link)
        except:
            pass
        
        # Return the link to the images
        return images
        
    ################################################################################
    # Function:         _get_price
    # Input:            tree
    # Output:           Price in euro
    # Goal:             Find the price and return it
    # Targets:          Use a css selecter to find the price
    # Example:          <span class="product-price">€145,00</span>
    def _get_price(self):
        price = ""
        try:
            price_meta = self._tree.cssselect('span[class*=\'product-price\']')
            price = unidecode(price_meta[0].text_content().strip().replace(',', '.'))
            price = price[3:]
        except:
            pass
        
        # Return the price
        return price
        
    def _get_currency(self):
        currency = ""
        try:
            # <meta content='EUR' itemprop="priceCurrency" />
            currency_meta = self._tree.cssselect('meta[itemprop*=\'priceCurrency\']')
            currency = currency_meta[0].attrib['content']
        except:
            pass
        
        # Return the currency
        return currency
        
    ################################################################################
    # Function:         _get_color
    # Input:            tree
    # Output:           Color
    # Goal:             Find the color and return it
    # Targets:          Use a css selecter to find the color
    # Example:          <h4 class="color-placeholder">Brown Suede</h4>
    def _get_color(self):
        color = ""
        try:
            # Use css to select to find the color
    	    color_meta = self._tree.cssselect('h4[class*=\'color-placeholder\']')
            # Save the price from the content field to the variable price
            color = unidecode(color_meta[0].text_content().strip())
        except:
            pass
        # Return the color
        return color
    
    ################################################################################
    # Function:         _get_title
    # Input:            tree
    # Output:           Title
    # Goal:             Find the title and return it
    # Targets:          Use a css selecter to find the title
    # Example:          <span itemprop="name">TEPHRA 2</span>
    def _get_title(self):
    	title = ""
    	try:
    	    # Use css to select the data
    	    title_data = self._tree.cssselect('span[itemprop*=\'name\']')
    	    # Retrieve the text from h1 and strip unwanted characters
    	    title = title_data[0].text_content().strip()
    	except:
    	    pass
        return title
    	
    ################################################################################
    # Function:         _get_category
    # Input:            tree
    # Output:           Category
    # Goal:             Find the category and return it
    # Targets:          Use reg ex to find the category
    # Example:          
    def _get_category(self):    
        category = ""
        try:
            category_meta = self._tree.cssselect('span[class*=\'category\']')
            category = category_meta[0].text_content().strip()
        except:
            pass    
        
        return category
    
    def _get_brand(self):
        # <a href="ted-baker" itemprop="brand">TED BAKER</a>
        brand = ""
        try:
            brand_data = self._tree.cssselect('a[itemprop*=\'brand\']')
            # Retrieve the text from h1 and strip unwanted characters
            brand = brand_data[0].text_content().strip()
        except:
            pass
        return brand
    
################################################################################
# main
################################################################################
def get_product(url):
    product = SarenzaProduct(url)
    return product