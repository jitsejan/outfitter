################################################################################
# Application:      Outfitter
# File:             topshop.py
# Goal:             topshop.py will retrieve specific information from a 
#                   given Topshop link and save the data to a variable
# Input:            url of website
# Output:           Target data
# Example:          info = crawl("http://eu.topman.com/en/tmeu/product/clothing-617800/mens-jumpers-cardigans-617811/charcoal-shawl-cardigan-4656120?bi=0&ps=20")
#
# History:          2015-09-28 - JJ     Creation of the file
#                   2015-10-29 - JJ     Added functionality to retrieve all images
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
appName =   "Topshop Crawler"

################################################################################
# Functions
################################################################################




################################################################################
# Classes
################################################################################

class TopshopProduct(Product):

    def __init__(self, *args, **kwargs):
        super(TopshopProduct,self).__init__('Topshop', *args, **kwargs)
        
    ################################################################################
    # Function:         _get_image
    # Input:            tree
    # Output:           URL of the image
    # Goal:             Find the image URL and return it
    # Targets:          Use a css selecter to find the image URL
    # Example:          Find <meta property="og:image" content="http://media.topman.com/wcsstore/TopManEU/images/catalog/81F22KCHR_normal.jpg"/>
    def _get_images(self):    
		images = []
		try:
			# Use css to select image
			image_data = self._tree.cssselect('meta[property*=\'og:image\']')
			# Save the image link from the content field to the variable image
			images.append(image_data[0].attrib['content'])
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
    # Example:          Find <span itemprop="offers"><meta itemprop="price" content="E 39,95">
    def _get_price(self):
		price = ""
		try:
			# Use css to select the meta-tag with name equal to twitter:data1
			price_meta = self._tree.cssselect('meta[property*=\'og:price:amount\']')
			# Save the price from the content field to the variable price
			price = price_meta[0].attrib['content']
		except:
			pass
		# Return the price
		return price
		
    def _get_currency(self):
		currency = ""
		try:
			currency_meta = self._tree.cssselect('meta[property*=\'og:price:currency\']')
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
    # Example:          Find <ul class="product_summary"><li class="product_colour">Colour:&nbsp;<span>GREY</span></li>
    def _get_color(self):
		color = ""
		try:
			# Use css to select to find the color
			color_meta = self._tree.cssselect('ul[class*=\'product_summary\'] li[class*=\'product_colour\'] span')
			# Save the price from the content field to the variable price
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
    # Example:          Find <div class="title"><h1>ASOS Jumper<h1>
    def _get_title(self):
		title = ""
		try:
			# Use css to select the meta-tag with name equal to description
			title_data = self._tree.cssselect('meta[property*=\'og:description\']')
			# Retrieve the text from h1 and strip unwanted characters
			title = title_data[0].attrib['content']
		except:
			pass
		# Return the title
		return title
    	
    ################################################################################
    # Function:         _get_category
    # Input:            self
    # Output:           Title
    # Goal:             Find the title and return it
    # Targets:          Use a css selecter to find the title
    # Example:          Find last word of description. There is no category explicitly
    def _get_category(self):
		category = ""
		try:
			# Use css to select the meta-tag with name equal to description
			category_data = self._tree.cssselect('meta[property*=\'og:description\']')
			# Retrieve the text and take the last word
			category = category_data[0].attrib['content'].rsplit(' ')[-1]
		except:
			pass
		# Return the title
		return category
		
    def _get_brand(self):
	    brand = ""
	    return brand	
################################################################################
# main
################################################################################
def get_product(url):
    product = TopshopProduct(url)
    return product
    
def get_price(url):
	product = TopshopProduct(url)
	return product.get_price()