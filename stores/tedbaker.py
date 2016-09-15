################################################################################
# Application:      Outfitter
# File:             tedbaker.py
# Goal:             tedbaker.py will retrieve specific information from a 
#                   given Ted Baker link and save the data to a variable
# Input:            url of website
# Output:           Ted Baker Product
# Example:          newProduct() = tedbaker.get_product("http://www.tedbaker.com/nl/Mens/Accessories/Bags/BOOMBAG-Colour-block-leather-messenger-bag-Oxblood/p/120731-41-OXBLOOD")
#
# History:          2015-09-28 - JJ     Creation of the file
#                   2015-10-07 - JJ     Changed structure to Product Class
#                   2015-10-28 - JJ     Added functionality to retrieve all images
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

class TedBakerProduct(Product):

    def __init__(self, *args, **kwargs):
        super(TedBakerProduct,self).__init__('Ted Baker', *args, **kwargs)
        
    ################################################################################
    # Function:         _get_images
    # Input:            tree
    # Output:           URL of the image
    # Goal:             Find the image URL and return it
    # Targets:          Use a css selecter to find the image URL
    # Example:          Find <div class="carousel" data-carousel="productImageCarousel"><div class="frame"><div class="viewport"><div class="slider" ng-class="{transition: transition}" ng-style="carouselView.style"><div class="image"><a class="image" href ng-click="galleryMode.id == 0 ? open() : null"><img src"link">
    def _get_images(self):
        images = []
        # Use css to select image
        try:
            image_data = self._tree.cssselect('section[id*=\"product_images\"] div[class*=\"carousel\"] div[class*=\"frame\"] div[class*=\"viewport\"] div[class*=\"slider\"] div[class*=\"image\"] a img')
            # Save the image links from the content field to the variable images
            for img in image_data:
                image = img.attrib['ng-src']
                # Replace the variable with a constant so the image can be displayed
                image = image.replace("{{imageFormat[view.imgSizes]['pdp_primary']}}", "w=460%26h=575%26q=85") 
                images.append(image)
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
    # Example:          Find <header id="product_head" class="lead"><ul class="pricing"><li class="price unit">E 345</li>
    def _get_price(self):
        price = ""
        try:
            price_meta = self._tree.cssselect('header[id*=\'product_head\'] ul[class*=\'pricing\'] li[class*=\'price\']')
            # Save the price from the content field to the variable price
            price = price_meta[0].text_content().strip()
            price = price[2:]
        except:
            pass
        # Return the price
        return price
        
    ################################################################################
    # Function:         _get_color
    # Input:            tree
    # Output:           Color
    # Goal:             Find the color and return it
    # Targets:          Use a css selecter to find the color
    # Example:          Find <div class="colours_switch" data-tid="colour_switch"><div class="frame"><ul><li class="selected"><span class="image" style="background-color: #b02a1c;" title="Oxblood">Oxblood</span>
    def _get_color(self):
        color = ""
        # Use css to select to find the color
        try:
            color_meta = self._tree.cssselect('div[class*=\'colours_switch\'] div[class*=\'frame\'] ul li[class*=\'selected\'] span[class*=\'image\']')
            # Save the price from the content field to the variable price
            color = color_meta[0].attrib['title']
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
    # Example:          Find <header id="product_head" class="lead"><hgroup><h1 class="name">BOOMBAG</h1>
    def _get_title(self):
    	title = ""
    	description = ""
    	# Use css to select the data
    	try:
    	    title_data = self._tree.cssselect('header[id*=\'product_head\'] hgroup h1[class*=\'name\']')
    	    # Retrieve the text from h1 and strip unwanted characters
    	    title = title_data[0].text_content().strip()
    	    
    	    desc_data = self._tree.cssselect('header[id*=\'product_head\'] hgroup h2[class*=\'summary\']')
    	    description = desc_data[0].text_content().strip()
    	except:
    	    pass
    	# Return the title
    	title += ' - ' + description
    	return title
    	
    ################################################################################
    # Function:         _get_category
    # Input:            tree
    # Output:           Category
    # Goal:             Find the category and return it
    # Targets:          Use reg ex to find the category
    # Example:          Find 'Knitwear' in
    #         var utag_data = {
    # 			error_count: storedErrorCount,
    # 			error_counter: storedErrorCounter,
    # 			site_territory : "Netherlands Site", product_price : "135.00", product_name : "03-CHARCOAL", site_region : "", country_code : "NL", user_name : "Anonymous", login_status : "logged out", site_country : "Netherlands Site", product_category : "Knitwear", site_currency : "EUR", product_code : "121420-03-CHARCOAL", page_type : "product_detail", site_section : "MALE", customer_new_returning : "return", page_name : "Basket stitch shawl neck jumper - Charcoal | Knitwear | Netherlands Site"
    # 		};
    def _get_category(self):    
        category = ""
        try:
            regexp = 'product_category : "(.*?)",'
            result = re.search(regexp, self._data)
            category = result.group(1)
        except:
            pass    
        
        return category
    
    ################################################################################
    # Function:         _get_currency
    # Input:            tree
    # Output:           Currency
    # Goal:             Find the currency and return it
    # Targets:          Use reg ex to find the currency
    # Example:          Find 'EUR' in
    #         var utag_data = {
    # 			error_count: storedErrorCount,
    # 			error_counter: storedErrorCounter,
    # 			site_territory : "Netherlands Site", product_price : "135.00", product_name : "03-CHARCOAL", site_region : "", country_code : "NL", user_name : "Anonymous", login_status : "logged out", site_country : "Netherlands Site", product_category : "Knitwear", site_currency : "EUR", product_code : "121420-03-CHARCOAL", page_type : "product_detail", site_section : "MALE", customer_new_returning : "return", page_name : "Basket stitch shawl neck jumper - Charcoal | Knitwear | Netherlands Site"
    # 		};
    def _get_currency(self):    
        currency = ""
        try:
            regexp = 'site_currency : "(.*?)",'
            result = re.search(regexp, self._data)
            currency = result.group(1)
        except:
            pass    
        
        return currency
        
    def _get_brand(self):
	    brand = "Ted Baker"
	    return brand
    
################################################################################
# main
################################################################################
def get_product(url):
    product = TedBakerProduct(url)
    return product