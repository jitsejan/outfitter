################################################################################
# Application:      Outfitter
# File:             clarks.py
# Goal:             clarks.py will retrieve specific information from a 
#                   given Clarks link and save the data to a variable
# Input:            url of website
# Output:           Clarks Product
# Example:          newProduct() = clarks.get_product("http://www.clarks.nl/p/26102898")
#
# History:          2015-10-13 - JJ     Creation of the file
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

class ClarksProduct(Product):

    def __init__(self, *args, **kwargs):
        super(ClarksProduct,self).__init__('Clarks', *args, **kwargs)
        
    ################################################################################
    # Function:         _get_image
    # Input:            tree
    # Output:           URL of the image
    # Goal:             Find the image URL and return it
    # Targets:          Use a css selecter to find the image URL
    # Example:          Find <div id="product-image"><img src="//assets.clarksmcr.com/products/2/6/1/26102898_A_p.jpg" alt="Clarks Raspin Brogue, Tabaksbruin Su&#232;de, Herenschoenen formeel" id="main-image" itemprop="image"/>
    def _get_images(self):
        images = []
        try:
            # Use css to select image
            image_data = self._tree.cssselect('div[id*=\"product-image\"] img[id*=\"main-image\"]')
            image_link = image_data[0].attrib['src']
            images.append(image_link)
            # Save the image link from the content field to the variable image
            regexp = 'ImagePath'
            result = re.findall(regexp, self._data)
            
            for i in range(2,len(result)):
                new_link = str.replace(image_link, '_A_', '_' + chr(64+i) +'_')
                images.append(new_link)

        except:
            pass
        
        # Return the link to the image
        return images
        
    ################################################################################
    # Function:         _get_price
    # Input:            tree
    # Output:           Price in euro
    # Goal:             Find the price and return it
    # Targets:          Use a css selecter to find the price
    # Example:          Find <input id="Price" name="Price" type="hidden" value="99,95" />
    def _get_price(self):
        price = ""
        try:
            price_meta = self._tree.cssselect('input[id*=\'Price\']')
            price = price_meta[0].attrib['value'].replace(',', '.')
        except:
            pass
        
        # Return the price
        return price
        
    def _get_currency(self):
        currency = ""
        try:
            # Find  <meta itemprop="priceCurrency" content="EUR">
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
    # Example:          Find <span class="colour" itemprop="color">Tabaksbruin Su&#232;de</span>
    def _get_color(self):
        color = ""
        try:
            # Use css to select to find the color
    	    color_meta = self._tree.cssselect('span[class*=\'colour\']')
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
    # Example:          Find <input id="ProductName" name="ProductName" type="hidden" value="Raspin Brogue" />
    def _get_title(self):
    	title = ""
    	try:
    	    # Use css to select the data
    	    title_data = self._tree.cssselect('input[id*=\'ProductName\']')
    	    # Retrieve the text from h1 and strip unwanted characters
    	    title = title_data[0].attrib['value']
    	except:
    	    pass
        return title
    	
    ################################################################################
    # Function:         _get_category
    # Input:            tree
    # Output:           Category
    # Goal:             Find the category and return it
    # Targets:          Use reg ex to find the category
    # Example:          Find <span class="category">Herenschoenen formeel</span>
    def _get_category(self):    
        category = ""
        try:
            category_meta = self._tree.cssselect('span[class*=\'category\']')
            category = category_meta[0].text_content().strip()
        except:
            pass    
        
        return category
    
    def _get_brand(self):
   		brand = "Clarks"
   		return brand
    
################################################################################
# main
################################################################################
def get_product(url):
    product = ClarksProduct(url)
    return product