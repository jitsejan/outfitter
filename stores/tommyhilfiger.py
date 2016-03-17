################################################################################
# Application:      Outfitter
# File:             tommyhilfiger.py
# Goal:             tommyhilfiger.py will retrieve specific information from a 
#                   given Tommy link and save the data to a variable
# Input:            url of website
# Output:           Tommy Hilfiger product
# Example:          newProduct = tommyhilfiger.get_product("http://nl.tommy.com/Melange-Duffle-Jas/0887883599,nl_NL,pd.html?q=duffle#!q%3Dduffle%26color%3D403%26size%3DS")
#
# History:          2015-09-29 - JJ     Creation of the file
#                   2015-10-07 - JJ     Changed structure to Product Class
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

class TommyHilfigerProduct(Product):

    def __init__(self, *args, **kwargs):
        super(TommyHilfigerProduct,self).__init__('Tommy Hilfiger', *args, **kwargs)

    ################################################################################
    # Function:         _get_images
    # Input:            tree
    # Output:           URL of the image
    # Goal:             Find the image URL and return it
    # Targets:          Use a css selecter to find the image URL
    # Example:          Find <meta itemprop="image" content="http://images.tommy.com/is/image/tommy/productlisting_04_0887883599_403?$productlisting$"/>
    def _get_images(self):
        images = []
        # Use css to select image
        image_data = self._tree.cssselect('ul[class*=\"productthumbnails\"] li[class*=\'thumbnail\'] img')
        # Save the image link from the content field to the variable image
        for image in image_data:
            image_link = str.replace(image.attrib['src'], 'thumb_new', 'zoom1_new')
            images.append(image_link)
        # Return the link to the image
        return images

    ################################################################################
    # Function:         _get_price
    # Input:            tree
    # Output:           Price in euro
    # Goal:             Find the price and return it
    # Targets:          Use a css selecter to find the price
    # Example:          Find <meta itemprop="currency" content="EUR" /><meta itemprop="price" content="429.0" />	
    def _get_price(self):
        price = ""
        # Use css to select the meta-tag with name equal to twitter:data1
        try:
            price_meta = self._tree.cssselect('meta[itemprop*=\'price\']')
            # Save the price from the content field to the variable price
            price = price_meta[0].attrib['content']
        except:
            pass # No price found
        return price

    def _get_currency(self):
        currency = ""
        try: 
            currency_meta = self._tree.cssselect('meta[itemprop*=\'pricCurrency\']')
            currency = currency_meta[0].attrib['content']
        except:
            pass # No currency found
        return currency
        
    ################################################################################
    # Function:         _get_color
    # Input:            self
    # Output:           Color
    # Goal:             Find the color and return it
    # Targets:          Use a css selecter to find the color
    # Example:          Find <div class="colorVariations swatches"><img alt="MIDNIGHT (Blauw)" src="http://images.tommy.com/is/image/tommy/colorSwatch_04_0887883599_403?$colorSwatch$"/>
    
    def _get_color(self):
        color = ""
        # Use css to select to find the color
        color_meta = self._tree.cssselect('div[class*=\'colorVariations\'] img')
        # Save the price from the content field to the variable price
        color = color_meta[0].attrib['alt']
        # Return the color
        return color
    
    ################################################################################
    # Function:         _get_title
    # Input:            self
    # Output:           Title
    # Goal:             Find the title and return it
    # Targets:          Use a css selecter to find the title
    # Example:          Find <h1 itemprop="name">Melange Duffle Jas</h1>
    def _get_title(self):
    	title = ""
    	# Use css to select the meta-tag with name equal to description
    	title_data = self._tree.cssselect('h1[itemprop*=\'name\']')
    	# Retrieve the text from h1 and strip unwanted characters
    	title = title_data[0].text_content().strip()
    	# Return the title
    	return title
    	
    ################################################################################
    # Function:         _get_category
    # Input:            self
    # Output:           Category
    # Goal:             Find the title and return it
    # Targets:          Use a css selecter to find the title
    # Example:          Find 'brighttagProductCategory = "Jassen &amp; Jacks"
    
    def _get_category(self):
    	category = ""
    	# Use regex to select the meta-tag with name equal to description
        regexp = 'brighttagProductCategory = "(.*)",'
        result = re.search(regexp, self._data)
        if result:
            category = result.group(1)
    	# Return the title
    	return category
    
    def _get_brand(self):
	    brand = "Tommy Hilfiger"
	    return brand
    	
################################################################################
# main
################################################################################
def get_product(url):
    product = TommyHilfigerProduct(url)
    return product