################################################################################
# Application:      Outfitter
# File:             sephora.py
# Goal:             sephora.py will retrieve specific information from a 
#                   given Clarks link and save the data to a variable
# Input:            url of website
# Output:           Clarks Product
# Example:          newProduct() = sephora.get_product("http://www.sephora.com/advanced-night-repair-synchronized-recovery-complex-ii-P379994?skuId=1551753")
#                   Italian site: http://www.sephora.it/Trattamenti-Viso/Antirughe-e-Antieta/Siero/Advanced-Night-Repair-Synchronized-Recovery-Complex-II/P1490005
#
# History:          2015-10-13 - JJ     Creation of the file
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

class SephoraProduct(Product):

    def __init__(self, *args, **kwargs):
        super(SephoraProduct,self).__init__('Sephora', *args, **kwargs)
        
    ################################################################################
    # Function:         _get_images
    # Input:            tree
    # Output:           URL of the image
    # Goal:             Find the image URL and return it
    # Targets:          Use a css selecter to find the image URL
    # Example:          Find "large_images":"/productimages/sku/s1551753-main-Lhero.jpg"
    def _get_images(self):
        images = []
        
        try:
            regexp = '"large_images":"(.*?)"'
            result = re.search(regexp, self._data)
            image = result.group(1)
            image_link = 'http://sephora.com'+image
            images.append(image_link)
        except:
            try:
                # Find <meta property="og:image" content="http://www.sephora.it/media/catalog_ProductCatalog/m6750793_P1490005_princ_hero.jpg" />
                image_meta = self._tree.cssselect('meta[property*=\'og:image\']')
                image = image_meta[0].attrib['content']
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
    # Targets:          Use regex to find the price
    # Example:          Find "list_price":(.*?),
    def _get_price(self):
        price = ""
        try: # Works for sephora.com
            regexp = '"list_price":(.*?),"'
            result = re.search(regexp, self._data)
            price = result.group(1)
        except:
            try: # Works for sephora.it
                # Find <input id="skuPrice0" 		type="hidden" 	value="85.90" />
                price_meta = self._tree.cssselect('input[id*=\'skuPrice\']')
                for p in price_meta:
                    price += p.attrib['value']
                    break # Only keep one price
            except:
                pass
       
            
        # Return the price
        return price
    
    def _get_currency(self): 
        currency = ""
        try:
            # Find <body id="product" ng-app="PDP" seph-currency="$" seph-save-cont-shopping data-social="true" data-at="pdp" data-ana-page="pdp">
            currency_meta = self._tree.cssselect('body[id*=\'product\']')
            currency = currency_meta[0].attrib['seph-currency']
            currency = 'USD'
        except:
            try:
                regexp = 'product_currency=\'(.*?)\''
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
    # Example:          Find 
    def _get_color(self):
        color = ""
        try: # Works for sephora.com
            regexp = '"variation_value":"(.*?)","'
            result = re.search(regexp, self._data)
            color = result.group(1)
        except:
            try: # Works for sephora.it
                # Find <input id="skuName0" 		type="hidden" 	value="30 ml" />
                color_meta = self._tree.cssselect('input[id*=\'skuName\']')
                for c in color_meta:
                    color += c.attrib['value']+','
                    break # Only keep one
            except:
                pass
        # Return the color
        return color
    
    ################################################################################
    # Function:         _get_title
    # Input:            tree
    # Output:           Title
    # Goal:             Find the title and return it
    # Targets:          Use regex to find the title
    # Example:          Find "display_name":"(.*?)"
    def _get_title(self):
    	title = ""
    	try:
    	    regexp = '"display_name":"(.*?)"'
            result = re.search(regexp, self._data)
            title = result.group(1)
    	except:
            try: 
                # Find  product_pid_name='Advanced Night Repair - Synchronized Recovery Complex II';
                regexp = 'product_pid_name=\'(.*?)\''
                result = re.search(regexp, self._data)
                title = result.group(1)
            except:
                pass
        return title
    	
    ################################################################################
    # Function:         _get_category
    # Input:            tree
    # Output:           Category
    # Goal:             Find the category and return it
    # Targets:          Use reg ex to find the category
    # Example:          Find "categoryPath=Skin Care,Treat,Face Serum & Treatments",
    def _get_category(self):    
        category = ""
        try:
            regexp = '"categoryPath=(.*?)"'
            result = re.search(regexp, self._data)
            category_meta = result.group(1).split(',')
            category = category_meta[-1]
        except:
            try:
                # Find tc_vars["page_sub_cat"]="Siero";
                regexp = 'tc_vars\["page_sub_cat"\]="(.*?)"'
                result = re.search(regexp, self._data)
                category = result.group(1)
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
    product = SephoraProduct(url)
    return product