################################################################################
# Application:      Outfitter
# File:             douglas.py
# Goal:             douglas.py will retrieve specific information from a 
#                   given Douglas link and save the data to a variable
# Input:            url of website
# Output:           Douglas Product
# Example:          newProduct() = douglas.get_product("https://www.douglas.nl/douglas/Verzorging-Gezicht-Serums-Est%C3%A9e-Lauder-Serums-Advanced-Night-Repair-Synchronized-Recovery-Complex-II_productbrand_3000052919.html?sourceRef=op3bBJ0Xt")
#
# History:          2015-10-11 - JJ     Creation of the file
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

class DouglasProduct(Product):

    def __init__(self, *args, **kwargs):
        super(DouglasProduct,self).__init__('Douglas', *args, **kwargs)
        
    ################################################################################
    # Function:         _get_images
    # Input:            tree
    # Output:           URL of the image
    # Goal:             Find the image URL and return it
    # Targets:          Use a css selecter to find the image URL
    # Example:          Find <div class="bigimage" style="z-index:0"><a href="https://media.douglas-shop.com/759917/900_0/Estee_Lauder-Serums-Advanced_Night_Repair_Synchronized_Recovery_Complex_II.jpg" class="cloud-zoom" id="zoom1" rel="adjustX: 10, adjustY:0" name="Article View" data-zoomtext="klik om te vergroten"><img src="https://media.douglas-shop.com/759917/300_0/Estee_Lauder-Serums-Advanced_Night_Repair_Synchronized_Recovery_Complex_II.jpg" width="300" height="300" alt="" /> <a href="https://media.douglas-shop.com/759917/900_0/Estee_Lauder-Serums-Advanced_Night_Repair_Synchronized_Recovery_Complex_II.jpg" class="cloud-zoom" id="zoom1" rel="adjustX: 10, adjustY:0" name="Article View" data-zoomtext="klik om te vergroten">                <img src="https://media.douglas-shop.com/759917/300_0/Estee_Lauder-Serums-Advanced_Night_Repair_Synchronized_Recovery_Complex_II.jpg" width="300" height="300" alt="" />
    def _get_images(self):
        images = []
        # Use css to select image
        image_data = self._tree.cssselect('div[class*=\"bigimage\"] a[class*=\'cloud-zoom\']')
        # Save the image link from the content field to the variable image
        images.append(image_data[0].attrib['href'])
        # Return the link to the image
        return images
        
    ################################################################################
    # Function:         _get_price
    # Input:            tree
    # Output:           Price in euro
    # Goal:             Find the price and return it
    # Targets:          Use a css selecter to find the price
    # Example:          Find pi.product_price="71.90";
    def _get_price(self):
        price = ""
        try:
            regexp = 'wt1.productCost="(.*?)"'
            result = re.search(regexp, self._data)
            price = result.group(1)
        except:
            pass 
        
        # Return the price
        return price
    
    def _get_currency(self):
        currency = ""
        try:
            regexp = 'pi.currency="(.*?)"'
            result = re.search(regexp, self._data)
            currency = result.group(1)
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
    # Example:          Find <div class="colorpalette"><div id="allVariantsSmall" class="clearfix colourSpots"><a href="/douglas/product_877540.html" id="smallVariant877540" name="Article to 877540" class="active"><img src="https://media.douglas-shop.com/877540/50/Estee_Lauder-Lippenmakeup-Pure_Color_Envy_Liquid_Lip_Potion.png" alt="120 - Extreme Nude"
    def _get_color(self):
        color = ""
        # Use css to select to find the color
    	try: # Colors are only valid for lipstick etcetera
    	    color_meta = self._tree.cssselect('div[class*=\'colorpalette\'] div[id*=\'allVariantsSmall\'] a[class*=\'active\'] img')
            # Save the price from the content field to the variable price
            color = color_meta[0].attrib['alt']
        except: # Find the quantity. Color not found
            #<div id="allVariantsSmall" class="clearfix"><a href="/douglas/product_759917.html" id="smallVariant759917" class="variantLabel sale layeropener active " name="Article to 759917">30 ml</a>
            try:
                color_meta = self._tree.cssselect('div[id*=\'allVariantsSmall\'] a[class*=\'active\']')
                color = color_meta[0].text_content().strip()
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
    # Example:          Find <p class="productname">Pure Color Envy Liquid Lip Potion</p>
    def _get_title(self):
    	title = ""
    	try:
    	    # Use css to select the data
    	    title_data = self._tree.cssselect('p[class*=\'product\']')
    	    # Retrieve the text from h1 and strip unwanted characters
    	    title = unicode(title_data[0].text_content().strip()).encode('ascii', 'xmlcharrefreplace')
    	except:
    	    pass
        return title
    	
    ################################################################################
    # Function:         _get_category
    # Input:            tree
    # Output:           Category
    # Goal:             Find the category and return it
    # Targets:          Use reg ex to find the category
    # Example:          Find Serums in pi.product_name="Serums";
    def _get_category(self):    
        category = ""
        try:
            regexp = 'pi.product_name="(.*?)"'
            result = re.search(regexp, self._data)
            category = result.group(1)
        except:
            pass    
        
        return category
    
    def _get_brand(self):
        brand = ""
        try:
            # Use css to select the data
            #  <img class="productbrand" id="producerLogo" src="https://media.douglas-shop.com/medias/sys_master/8469813281986928.gif" alt="DIOR" />
            brand_data = self._tree.cssselect('img[id*=\'producerLogo\']')
            # Retrieve the text from h1 and strip unwanted characters
            brand = brand_data[0].attrib['alt']
        except:
            pass
        return brand.capitalize()

################################################################################
# main
################################################################################
def get_product(url):
    product = DouglasProduct(url)
    return product
