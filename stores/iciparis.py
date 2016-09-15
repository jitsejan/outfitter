################################################################################
# Application:      Outfitter
# File:             iciparis.py
# Goal:             iciparis.py will retrieve specific information from a 
#                   given Ici Paris XL link and save the data to a variable
# Input:            url of website
# Output:           Ici Paris XL Product
# Example:          newProduct() = iciparis.get_product("http://www.iciparisxl.nl/nl_NL/-/-/ADVANCED-NIGHT-REPAIR-SYNCHRONIZED-RECOVERY-COMPLEX-II/p636227-ZOup_hmDAKYAAAEhNBweqNPff")
#
# History:          2015-10-11 - JJ     Creation of the file
#
################################################################################

################################################################################
# Imports
################################################################################
from product import Product
import re, unidecode

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

class IciParisProduct(Product):

    def __init__(self, *args, **kwargs):
        super(IciParisProduct,self).__init__('Ici Paris XL', *args, **kwargs)
        
    ################################################################################
    # Function:         _get_images
    # Input:            tree
    # Output:           URL of the image
    # Goal:             Find the image URL and return it
    # Targets:          Use a css selecter to find the image URL
    # Example:          Find <div class="productimage"><img src="http://www.iciparisxl.nl:80/is-bin/intershop.static/WFS/IPXL-IPNL-Site/IPXL/nl_NL/products/large/27131264637.jpg" name="ADVANCED NIGHT REPAIR SYNCHRONIZED RECOVERY COMPLEX II" title="ADVANCED NIGHT REPAIR SYNCHRONIZED RECOVERY COMPLEX II" alt="ADVANCED NIGHT REPAIR SYNCHRONIZED RECOVERY COMPLEX II">
    def _get_images(self):
        images = []
        try:
        # Use css to select image
            image_data = self._tree.cssselect('div[class*=\"productimage\"] img')
        # Save the image link from the content field to the variable image
            images.append(image_data[0].attrib['src'])
        # Return the link to the image
        except:
            pass
        return images
        
    ################################################################################
    # Function:         _get_price
    # Input:            tree
    # Output:           Price in euro
    # Goal:             Find the price and return it
    # Targets:          Use a css selecter to find the price
    # Example:          Find <span class="yourprice">Uw prijs: <span class="amount">&#8364; 72,99</span></span>
    def _get_price(self):
        price = ""
        try:
            price_meta = self._tree.cssselect('span[class*=\'yourprice\'] span[class*=\'amount\']')
        # Save the price from the content field to the variable price
            price = price_meta[0].text_content().strip()
        
            price = price[2:].replace(',', '.')
        except:
            pass
        # Return the price
        return price
    
    def _get_currency(self):
        currency = "EUR"
        # Return the currency
        return currency
        
    ################################################################################
    # Function:         _get_color
    # Input:            tree
    # Output:           Color
    # Goal:             Find the color and return it
    # Targets:          Use a css selecter to find the color
    # Example:          Find 
    def _get_color(self):
        color = ""
        try:
        # Use css to select to find the color
    	    color_meta = self._tree.cssselect('div[class*=\'variations\'] div[class*=\'variation\'] div[class*=\'details\'] span')
        # Save the price from the content field to the variable price
            color = unicode(color_meta[1].text_content().strip().replace('\n\n', ': ')).encode('ascii', 'xmlcharrefreplace')
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
    # Example:          Find<div class="variations"><span class="title">Product informatie</span><div class="variation"><div class="details makeup"><span class="name">SKIN ILLUSION LOOSE POWDER FOUNDATION</span>
    def _get_title(self):
    	title = ""
    	# Use css to select the data
    	# <meta name="description" content="N&deg;5." />
        try:
    	    title_data = self._tree.cssselect('meta[name*=\'description\']')
    	# Retrieve the text from h1 and strip unwanted characters
    	    title = unicode(title_data[0].attrib['content']).encode('ascii', 'xmlcharrefreplace')
    	except:
    	    pass
        return title
    	
    ################################################################################
    # Function:         _get_category
    # Input:            tree
    # Output:           Category
    # Goal:             Find the category and return it
    # Targets:          Use reg ex to find the category
    # Example:          Find Foundation in 'list': 'Catalog page | Foundation'
    def _get_category(self):    
        category = ""
        try:
            regexp = "'list': 'Catalog page \| (.*)'"
            result = re.search(regexp, self._data)
            category = unicode(result.group(1)).encode('ascii', 'xmlcharrefreplace')
        except:
            pass    
        
        return category
    
    def _get_brand(self):
        brand = ""
        try:
            regexp = "'brand': '(.*)'"
            result = re.search(regexp, self._data)
            brand = unicode(result.group(1)).encode('ascii', 'xmlcharrefreplace')
        except:
            pass    
        return brand.capitalize()
    
################################################################################
# main
################################################################################
def get_product(url):
    product = IciParisProduct(url)
    return product
