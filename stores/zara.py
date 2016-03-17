################################################################################
# Application:      Outfitter
# File:             zara.py
# Goal:             zara.py will retrieve specific information from a 
#                   given Zara link and save the data to a variable
# Input:            url of website
# Output:           Zara Product
# Example:          newProduct = zara.get_product("www.zara.com/nl/nl/heren/sweatshirts/-c309502p2979528.html")
#
# History:          2015-09-11 - JJ     Creation of the file
#                   2015-10-07 - JJ     Changed structure to Product Class
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
appName =   "Zara Crawler"

################################################################################
# Functions
################################################################################

################################################################################
# Classes
################################################################################

class ZaraProduct(Product):

    def __init__(self, *args, **kwargs):
        super(ZaraProduct,self).__init__('Zara', *args, **kwargs)

    ################################################################################
    # Function:         _get_image
    # Input:            tree
    # Output:           URL of the image
    # Goal:             Find the image URL and return it
    # Targets:          Use a css selecter to find the image URL
    # Example:          Find <meta name="twitter:image" content="fullink"> and
    #                   return fulllink
    def _get_images(self):
        images = []
        # Use css to select the meta-tag with name equal to twitter:image
        try:
            image_data = self._tree.cssselect('img[class*=\"image-big\"]')
            for image in image_data:
                # Save the image link from the content field to the variable image
                images.append(image.attrib['data-src'])
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
    # Example:          Find <p class="price"><span class="price" date-price="39,95  EUR">
    def _get_price(self):
        price = ""
        # Use css to select the meta-tag with name equal to twitter:data1
        try:
            price_meta = self._tree.cssselect('p[class*=\'price\'] span[class*=\'price\']')
            # Save the price from the content field to the variable price
            price = price_meta[0].attrib['data-price']
            price = price[:-5]
        except:
            try:
                price_meta = self._tree.cssselect('p[class*=\'price\'] span[class*=\'sale\']')
                # Save the price from the content field to the variable price
                price = price_meta[0].attrib['data-price']
                price = price[:-5].replace(',', '.')
            except:
                pass
        # Return the price
        return price
    
    def _get_currency(self):
        currency = ""
        # Use css to select the meta-tag with name equal to twitter:data1
        try:
            currency_meta = self._tree.cssselect('p[class*=\'price\'] span[class*=\'price\']')
            # Save the price from the content field to the variable price
            currency = price_meta[0].attrib['data-price']
            currency = currency[-4:]
        except:
            try:
                currency_meta = self._tree.cssselect('p[class*=\'price\'] span[class*=\'sale\']')
                # Save the price from the content field to the variable price
                currency = currency_meta[0].attrib['data-price']
                currency = currency[-4:]
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
    # Example:          Find <div class="colors"><label><div title="Marineblauw">
    def _get_color(self):
        color = ""
        # Use css to select the meta-tag with name equal to twitter:data2
        try:
            color_meta = self._tree.cssselect('div[class*=\'colors\'] label div')
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
    # Example:          Find <meta name="description" content="T-SHIRT MET TEKST" />
    def _get_title(self):
        title = ""
        # Use css to select the meta-tag with name equal to description
        try:
            title_data = self._tree.cssselect('meta[name*=\'description\']')
            if title_data:
                # Retrieve the text from h1 and strip unwanted characters
                title = title_data[0].attrib['content']
            else:
                title = '-'
        except:
            pass
        # Return the title
        return title  
    
    ################################################################################
    # Function:         _get_category
    # Input:            tree
    # Output:           Title
    # Goal:             Find the title and return it
    # Targets:          Use a css selecter to find the title
    # Example:          Find <div class="breadcrumbs" itemprop="breadcrumb"><ul><li><a href="http://www.zara.com/"><span>ZARA</span></a><span class="breadCrumptSeparator"> > </span></li><li itemscope itemtype="http://data-vocabulary.org/Breadcrumb"><a href="http://www.zara.com/nl/nl/heren-c292503.html" itemprop="url"><span itemprop="title">HEREN</span></a>

    def _get_category(self):
        category = ""
        # Use css to select the meta-tag with name equal to description
        try:
            category_data = self._tree.cssselect('div[class*=\'breadcrumbs\'] ul li[itemtype*=\"http://data-vocabulary.org/Breadcrumb\"] a[itemprop*=\'url\'] span[itemprop*=\'title\']')
            # Retrieve the text from h1 and strip unwanted characters
            index = 1 #len(category_data)
            category = category_data[index].text_content().strip()
        except:
            pass
        # Return the title
        return category
    
    def _get_brand(self):
	    brand = "Zara"
	    return brand

################################################################################
# main
################################################################################
def get_product(url):
    product = ZaraProduct(url)
    return product