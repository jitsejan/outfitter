################################################################################
# Application:      Outfitter
# File:             netaporter.py
# Goal:             
# Input:            
# Output:           
# Example:          
#
# History:          2016-03-01 - JJ     Creation of the file
#
################################################################################

################################################################################
# Imports
################################################################################
from tracker import Tracker
import orm, olog
import json
import lxml.html
import re, time
import shortuuid
import urllib2
import lxml.etree
import unidecode

from pyvirtualdisplay import Display
from selenium import webdriver

################################################################################
# Definitions
################################################################################
author =    "JJ"
appName =   "Outfitter"
hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729); nl-NL'}
################################################################################
# Functions
################################################################################

################################################################################
# Classes
################################################################################

class NetaporterTracker(Tracker):

    def __init__(self, *args, **kwargs):
        super(NetaporterTracker,self).__init__('Net-a-Porter', *args, **kwargs)

    #############################################################################
    # Function:         _get_brands
    # Input:            
    # Output:           
    # Goal:             
    # Targets:           
    
    def _set_brands(self, session, insert):
        global hdr
        brands = []
            
        brandsUrl = "https://www.net-a-porter.com/de/en/Shop/AZDesigners?cm_sp=topnav-_-designers-_-designera-z"
        gender = "female"
        olog.log("NetaporterTracker._set_brands > Calling <b>"+brandsUrl+"</b>", 'info')
        
        req = urllib2.Request(brandsUrl, headers=hdr)
        data = urllib2.urlopen(req).read()
        tree = lxml.html.fromstring(data)
        
        brand_data = tree.cssselect('div[class=\"designer_list_col\"] ul li[class!=\"top-letter\"] a')
        for b in brand_data:
            brand = {'key' : None, 'name' : None, 'logoUrl' : None, 'logoLargeUrl' : None, 'shopUrl' : None}
            brand['shopUrl'] = 'http://www.net-a-porter.com'+b.attrib['href']+"?pn=1&npp=view_all&image_view=product&dScroll=0"
            brand['name'] = unicode(b.attrib['title'].title()).encode('ascii', 'xmlcharrefreplace')
        
            brand_in_db = session.query(orm.Brand).filter_by(name=unicode(brand['name'])).first()
            if brand_in_db is None:
                uuid = str(shortuuid.uuid(brand['name']))
                br = orm.Brand(brand['name'], brand['logoUrl'], brand['logoLargeUrl'], uuid)
                olog.log("NetaporterTracker._set_brands <<< Inserted brand <b>"+str(br)+"</b> with id <b>" + str(br.id) + "</b>", "warning")
                if insert is True:
                    session.add(br)
                    session.flush()
                    brandid = br.id
            else:
                br = brand_in_db
                olog.log("NetaporterTracker._set_brands <<< Brand <b>"+str(brand_in_db)+"</b> already in database", "info")                
                brandid = brand_in_db.id

              
            storebrand_in_db = session.query(orm.StoreBrand).filter_by(storeid=unicode(self.storeid)).filter_by(brandid=brandid).filter_by(gender=gender).first()
            
            if storebrand_in_db is None:
                storebrand = {'key': None, 'storeid' : None, 'brandid' : None, 'gender': None, 'url' : None}
                sb = orm.StoreBrand(brand['key'], self.storeid, brandid, gender, brand['shopUrl'])
                olog.log("NetaporterTracker._set_brands <<< Inserted <b>"+str(sb)+"</b>", "warning")
                if insert is True:
                    session.add(sb)
                    session.flush()
            else:
                olog.log("NetaporterTracker._set_brands <<< <b>"+str(storebrand_in_db)+"</b> already in database", "info")
        
            brands.append(br)
        
        session.commit()

        return brands

    def _set_items_for_brand(self, brand, session, insert):
        global hdr
        items = []
        
        display = Display(visible=0, size=(1920, 1080))
        display.start()
        browser = webdriver.Firefox()
        
        date = time.strftime('%Y-%m-%d %H:%M:%S')
        olog.log("NetaporterTracker._set_items_for_brand >>> Get articles <b>"+brand.url+"</b>", 'debug')
        # try:
        req = urllib2.Request(brand.url, headers=hdr)
        data = urllib2.urlopen(req).read()
        tree = lxml.html.fromstring(data)
    
        items_data = tree.cssselect('div[id=\"product-list\"] div[class=\"product-images\"] div[class*=\"product-image\"] a')
        for it in items_data:
            iid = re.search('/product/(.*?)/', it.attrib['href']).group(1)
            i = session.query(orm.Item).filter_by(itemid=iid).filter_by(storeid=self.storeid).first()
            if i is None:
                item = self._get_item(brand, it.attrib['href'], browser, display)
                if item:
                    i = orm.Item(item['storeid'], item['itemid'], item['brandid'], item['link'], item['color'], item['title'], item['category'], item['gender'], item['uuid'])
                    olog.log("NetaporterTracker._set_items_for_brand <<< Inserted item <b>"+str(i)+"</b>>", "warning")
                    if insert is True:
                        session.add(i)
                        session.flush()
                        itemid = i.id
                        for imageurl in item['images']:
                            ii = orm.ItemImage(itemid, imageurl)
                            olog.log("NetaporterTracker._set_items_for_brand <<<< Inserted image <b>"+str(ii)+"</b>", "warning")
                            if insert is True:     
                                session.add(ii)
                        ip = orm.ItemPrice(itemid, item['price'], item['currency'], date)
                        olog.log("NetaporterTracker._set_items_for_brand <<<< Inserted price <b>"+str(ip)+"</b>", "warning")
                        if insert is True:
                            session.add(ip)                      
                else:
                    olog.log("NetaporterTracker._set_items_for_brand <<<< Error getting item", "error")
            else:
                olog.log("NetaporterTracker._set_items_for_brand <<< <b>"+str(i)+"</b> already in database</b>", "info")
            #endif i is None
            items.append(i)
            
            # break
        #endfor it in items_data 

      
        if insert is True:
            session.commit()
        # # except:
        # #     olog.log("BijenkorfTracker._set_items_for_brand <<< Error opening URL", 'error')
        browser.quit()
        display.stop()
           
        return items
        
    def _get_item(self, brand, url, browser, display):
        global hdr
        item = {'storeid' : None, 'itemid' : None, 'brandid' : None, 'link' : None, 'color' : None, 'title' : None, 'category' : None, 'gender' : None}
        item['storeid'] = self.storeid
        if 'net-a-porter.com' not in url:
            url = 'http://www.net-a-porter.com'+url
        url = url.replace('product', 'nl/en/product')
        item['link'] = url
        item['brandid'] = brand.brandid
        item['gender'] = brand.gender.title()
        item['itemid'] = re.search('/product/(.*?)/', url).group(1)
        item['uuid'] = str(shortuuid.uuid(item['link']))
        olog.log("NetaporterTracker._get_item >>>> Calling <b>"+item['link']+"</b>", "debug")
        
        browser.get(item['link'])
        idata = browser.page_source
        
        itree = lxml.html.fromstring(idata)
        
        item['images'] = self._get_images(itree)
        item['price'] = self._get_price(itree)
        item['currency'] = self._get_currency(itree)
        item['color'] = self._get_color(itree)
        item['title'] = self._get_title(itree)
        item['category'] = self._get_category(itree)
        if item['color'] == "":
            return False
        return item
    
    def _get_images(self, itree):
        images = []
        try:
            image_data = itree.cssselect('li[class*=\"swiper-slide-duplicate\"] img')
            for image in image_data:
                try:
                    imageurl = image.attrib['src']
                    if 'http' not in imageurl:
                        imageurl = imageurl.replace('//', 'http://')
                    if imageurl not in images and 'pp' in imageurl:
                        images.append(imageurl)
                except:
                    pass # false positive
            # Return the links to the images
        except:
            pass
        return images
    
    def _get_price(self, itree):
        try:
            return itree.cssselect('span[itemprop=\'price\']')[0].attrib['content'].replace(',', '')
        except:
            return ""
    
    def _get_currency(self, itree):
        try:
            return itree.cssselect('span[itemprop*=\'priceCurrency\']')[0].attrib['content']
        except:
            return ""
    
    def _get_color(self, itree):
        try:
            color_data = itree.cssselect('widget-show-hide[id=\'accordion-2\'] ul[class*=\'font-list-copy\'] li')
            color = color_data[0].text_content()[1:].split(' ')[1].strip()
            #TODO
            print color
            available_colors = ['Merlot', 'Nude', 'Beige', 'Indigo', 'Platinum', 'Lobster', 'Rust', 'Mint', 'Ecru', 'Coral', 'Orange', 'Charcoal', 'Navy', 'Saffron', 'Tortoise', 'Rose', 'Sand', 'Ecru', 'Claret', 'Blush', 'Gray', 'Taupe', 'Papaya', 'Tan', 'Tangerine', 'Ivory', 'Brown', 'Gold', 'Red', 'Pink', 'Green', 'Black', 'Multicolored', 'Blue', 'Silver', 'Yellow', 'Aqua', 'Violet', 'Purple', 'White', 'Pale']
            if any(c.upper() in color.upper() for c in available_colors):
                return unicode(color.replace(',', '').title()).encode('ascii', 'xmlcharrefreplace')
            else:
                color2 = color_data[1].text_content()[1:].split(' ')[1].strip()
                print color2
                if any(c2.upper() in color2.upper() for c2 in available_colors):
                    return unicode(color2.replace(',', '').title()).encode('ascii', 'xmlcharrefreplace')
                else:
                    return ""
        except:
            return ""
        
    def _get_title(self, itree):
        try:
            return unicode(itree.cssselect('meta[itemprop*=\'name\']')[0].attrib['content'].strip().title()).encode('ascii', 'xmlcharrefreplace')
        except:
            return ""
    
    def _get_category(self, itree):    
        try:
            return unicode(itree.cssselect('meta[itemprop*=\'category\']')[0].attrib['content'].split('/')[-2].strip().title()).encode('ascii', 'xmlcharrefreplace')
        except:
            return ""     
