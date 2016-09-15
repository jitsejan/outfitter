################################################################################
# Application:      Outfitter
# File:             zalando.py
# Goal:             zalando.py will retrieve specific information from a 
#                   given Zalando link and save the data to a variable
# Input:            url of website
# Output:           Zalando Product
# Example:          newProduct = zalando.get_product("https://m.zalando.nl/ted-baker-illion-colbert-grey-te422b002-c11.html")
#
# History:          2015-09-12 - JJ     Creation of the file
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

class ZalandoProduct(Product):

    def __init__(self, *args, **kwargs):
        super(ZalandoProduct,self).__init__('Zalando', *args, **kwargs)

    ################################################################################
    # Function:         _get_images
    # Input:            json data
    # Output:           URL of the image
    # Goal:             Find the image URL and return it
    # Targets:          Use a regex to find "image" : "url"
    #
    def _get_images(self):
        images = []
        try:
            # Use regex to find the image in the json data
            regexp = '"image" : "(.*)",'
            result = re.search(regexp, self._data)
            if result:
                image = result.group(1)
                images.append(image)
                
            # <img src="https://secure-i5.ztat.net//detail/PI/92/2Q/A0/QK/11/PI922QA0Q-K11@8.jpg" alt="" class="articleMedia_markupImage" />
            image_data = self._tree.cssselect('img[class*=\'articleMedia_markupImage\']')
            for image_d in image_data:
                # Save the image link from the content field to the variable image
                # Replace detail with large to retrieve the large image
                image_link = str.replace(image_d.attrib['src'], 'detail', 'large')
                images.append(image_link)
        except:
            pass
        # Return the link to the image
        return images
        
    ################################################################################
    # Function:         _getPrice
    # Input:            tree
    # Output:           Price in euro
    # Goal:             Find the price and return it
    # Targets:          Use a regex to find "price" : "999.99"
    #
    def _get_price(self):
        price = ""
        # Use regex to find the image in the json data
        try:
            regexp = '"price" : "(.*)",'
            result = re.search(regexp, self._data)
            if result:
                price = result.group(1)
        except:
            pass
        # Return the price
        return price

    def _get_currency(self):
        # <meta itemprop="priceCurrency" content="EUR" />
        try:
            return self._tree.cssselect('meta[itemprop*=\'priceCurrency\']')[0].attrib['content']
        except:
            return ""
        
    ################################################################################
    # Function:         _getColor
    # Input:            tree
    # Output:           Color
    # Goal:             Find the color and return it
    # Targets:          Use regex to find the color
    # 
    def _get_color(self):
        color = ""
        try:
            # Use regex to find the image in the json data
            regexp = '"color" : "(.*)",'
            result = re.search(regexp, self._data)
            color = result.group(1)
        except:
            pass
        # Return the color
        return color
    
    ################################################################################
    # Function:         _getTitle
    # Input:            tree
    # Output:           Title
    # Goal:             Find the title and return it
    # Targets:          Use regex to find the title
    #
    def _get_title(self):
        title = ""
        regexp = '"name" : "(.*)",'
        try:
            result = re.search(regexp, self._data)
            title = result.group(1)
        except:
            pass
        # Return the title
        return title
    
    ################################################################################
    # Function:         _getCategory
    # Input:            tree
    # Output:           Category
    # Goal:             Find the category and return it
    # Targets:          Use css selector to find the category
    # Example:          Find 'Truien & vesten' in
    #        wtpl.productCategory = {.*,"3":"(.*)","4"
    
    def _get_category(self):    
        category = ""
        regexp = 'wtpl.productCategory = {.*,"3":"(.*)","4"'
        result = re.search(regexp, self._data)
        if result:
            category = result.group(1)
        return category        
   
	################################################################################
    # Function:         _get_brand
    # Input:            tree
    # Output:           brand
    # Goal:             Find the color and return it
    # Targets:          Use regex to find the color
    # 
    def _get_brand(self):
        brand = ""
        try:
            # Use regex to find the brand in the json data
            regexp = '"manufacturer" : "(.*)",'
            result = re.search(regexp, self._data)
            brand = result.group(1)
        except:
            pass
        # Return the color
        return brand     
        
################################################################################
# main
################################################################################
def get_product(url):
    product = ZalandoProduct(url)
    return product