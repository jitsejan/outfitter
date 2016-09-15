# -*- coding: utf-8 -*-
################################################################################
# Application:      Outfitter
# File:             asos.py
# Goal:             asos.py will retrieve specific information from a 
#                   given Asos link and save the data to a variable
# Input:            url of website
# Output:           Asos Product
# Example:          newProduct = asos.get_product("http://www.asos.com/ASOS/ASOS-Jumper-with-Fluffy-Yarn-and-Grid-Check/Prod/pgeproduct.aspx?iid=5221446&cid=13531&sh=0&pge=0&pgesize=36&sort=-1&clr=White&totalstyles=111&gridsize=3")
#
# History:          2015-09-11 - JJ     Creation of the file
#                   2015-10-07 - JJ     Changed structure to Product Class
#                   2015-10-28 - JJ     Added functionality to retrieve all images
#
################################################################################

################################################################################
# Imports
################################################################################
from product import Product

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

class AsosProduct(Product):

    def __init__(self, *args, **kwargs):
        super(AsosProduct,self).__init__('Asos', *args, **kwargs)
        
    ################################################################################
    # Function:         _get_images
    # Input:            tree
    # Output:           URL of the images
    # Goal:             Find the image URLs and return them
    # Targets:          Use a css selecter to find the image URL
    # Example:          Find <div id="productImages"><div class="productImagesItems"><div class="image1"><img src="url">
    def _get_images(self):
        images = []
        
        try:
            # Use css to select image
            image_data = self._tree.cssselect('div[id*=\"productImages\"] div[class*=\"productImagesItems\"] div[class*=\"image\"] img')
            for image in image_data:
                try:
                    # Save the image link from the content field to the variable images
                    images.append(image.attrib['src'])
                except:
                    pass # false positive
            # Return the links to the images
        except:
            pass
        return images
        
    ################################################################################
    # Function:         _get_price
    # Input:            tree
    # Output:           Price in euro
    # Goal:             Find the price and return it
    # Targets:          Use a css selecter to find the price
    # Example:          Find <span itemprop="offers"><meta itemprop="price" content="E 39,95">
    def _get_price(self):
        price = ""
        try:
            # Use css to select the meta-tag with name equal to twitter:data1
            price_meta = self._tree.cssselect('span[itemprop*=\'offers\'] meta[itemprop*=\'price\']')
            # Save the price from the content field to the variable price
            price = price_meta[0].attrib['content']
            # Remove the EUR after the price (last three characters) 
            price = price[1:]
        except:
            pass
        # Return the price
        return price
        
    
    def _get_currency(self):
        currency = ""
        try:
            price_meta = self._tree.cssselect('span[itemprop*=\'offers\'] meta[itemprop*=\'price\']')
            price = price_meta[0].attrib['content']
            
            if u"£" in price:
                currency = 'GBP'
            elif u"€" in price:
                currency = 'EUR'
            elif u"$" in price:
                currency = "USD"
                
        except:
            pass
        return currency
        
    ################################################################################
    # Function:         _get_color
    # Input:            tree
    # Output:           Color
    # Goal:             Find the color and return it
    # Targets:          Use a css selecter to find the color
    # Example:          Find <div class="colors"><label><div title="Marineblauw">
    def _get_color(self):
        color = ""
        try:
            # Use css to select to find the color
            color_meta = self._tree.cssselect('div[class*=\'colour\'] option[selected*=\'selected\']')
            # Save the price from the content field to the variable price
            color = color_meta[0].attrib['value']
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
    # Example:          Find <div class="title"><h1>ASOS Jumper<h1>
    def _get_title(self):
    	title = ""
    	try:
    	    # Use css to select the meta-tag with name equal to description
    	    title_data = self._tree.cssselect('div[class*=\'title\'] h1')
    	    # Retrieve the text from h1 and strip unwanted characters
    	    title = title_data[0].text_content().strip()
    	except:
    	    pass
    	# Return the title
    	return title
    
    ################################################################################
    # Function:         _get_category
    # Input:            tree
    # Output:           Category
    # Goal:             Find the category and return it
    # Targets:          Use css selector to find the category
    # Example:          Find Boots in <div id="ctl00_ContentMainPage_productInfoPanel" class="ui-tabs-panel product-description"><a href=" /Men/Shoes-Boots-Trainers/Boots/Cat/pgecategory.aspx?cid=5774"><strong>Boots</strong></a>
    
    def _get_category(self):    
        category = ""
        try:
            category_data = self._tree.cssselect('div[id*=\'ctl00_ContentMainPage_productInfoPanel\'] strong')
    	    # Retrieve the text from h1 and strip unwanted characters
            if category_data:
                category = category_data[0].text_content().strip()
        except:
            pass
        return category        
   
    def _get_brand(self):
	    brand = ""
	    return brand
        
################################################################################
# main
################################################################################
def get_product(url):
    product = AsosProduct(url)
    return product
    
