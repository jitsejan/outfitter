# -*- coding: utf-8 -*-
################################################################################
# Application:      Outfitter
# File:             clarks.py
# Goal:             
# Input:            
# Output:           
# Example:          
#
# History:          2016-02-16 - JJ     Creation of the file
#
################################################################################

################################################################################
# Imports
################################################################################
from tracker import Tracker
import orm, olog
import json
import re
import lxml.html
import shortuuid
import time
import urllib2
import unidecode

from pyvirtualdisplay import Display
from selenium import webdriver

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

class ClarksTracker(Tracker):

    def __init__(self, *args, **kwargs):
        super(ClarksTracker,self).__init__('Clarks', *args, **kwargs)

    ############################################################################
    # Function:         _set_brands
    # Input:            self, session, insert
    # Output:           brands
    # Goal:             
    # Targets:
    # 
    def _set_brands(self, session, insert):
        brands = []
        
        brand = {'key' : None, 'name' : None, 'logoUrl' : None, 'logoLargeUrl' : None, 'shopUrl' : None}
        brand['name'] = 'Clarks' # Fixed. Website only sells Clarks
        brand['shopUrl'] = 'http://www.clarks.nl/c/heren-alle-stijlen'
        uuid = str(shortuuid.uuid(brand['name']))
        gender = 'Male'
        br = orm.Brand(brand['name'], brand['logoUrl'], brand['logoLargeUrl'], uuid)
        olog.log("ClarksTracker._set_brands << Found brand <b>"+str(br)+"</b>", 'debug')

        brand_in_db = session.query(orm.Brand).filter_by(name=unicode(br.name)).first()
        if brand_in_db is None:
            if insert is True:
                session.add(br)
                session.flush()
                brandid = br.id
                olog.log("ClarksTracker._set_brands >>> Inserted brand <b>"+br.name+"</b> with id <b>" + str(brandid) + "</b>", "warning")
        else:
            brandid = brand_in_db.id
            olog.log("ClarksTracker._set_brands << Brand <b>"+brand_in_db.name+"</b> already in database with id <b>" + str(brandid) + "</b>", "info")
                
        storebrand_in_db = session.query(orm.StoreBrand).filter_by(storeid=unicode(self.storeid)).filter_by(brandid=brandid).filter_by(gender=gender).first()
        if storebrand_in_db is None:
            storebrand = {'key': None, 'storeid' : None, 'brandid' : None, 'gender' : None, 'url' : None}
            sb = orm.StoreBrand(brand['key'], self.storeid, brandid, gender, brand['shopUrl'])
            olog.log("ClarksTracker._set_brands << Inserted <b>"+str(sb)+"</b>", "warning")
            if insert is True:
                session.add(sb)
                session.flush()
        else:
            olog.log("ClarksTracker._set_brands << StoreBrand <b>"+str(storebrand_in_db)+"</b> already in database with id <b>" + str(storebrand_in_db.id) + "</b>", "info")
            
        brands.append(br)

        brand = {'key' : None, 'name' : None, 'logoUrl' : None, 'logoLargeUrl' : None, 'shopUrl' : None}
        brand['name'] = 'Clarks' # Fixed. Website only sells Clarks
        brand['shopUrl'] = 'http://www.clarks.nl/c/dames-alle-stijlen'
        uuid = str(shortuuid.uuid(brand['name']))
        gender = 'Female'
        br = orm.Brand(brand['name'], brand['logoUrl'], brand['logoLargeUrl'], uuid)
        olog.log("ClarksTracker._set_brands << Found brand <b>"+str(br)+"</b>", 'debug')

        brand_in_db = session.query(orm.Brand).filter_by(name=unicode(br.name)).first()
        if brand_in_db is None:
            if insert is True:
                session.add(br)
                session.flush()
                brandid = br.id
                olog.log("ClarksTracker._set_brands >>> Inserted brand <b>"+br.name+"</b> with id <b>" + str(brandid) + "</b>", "warning")
        else:
            brandid = brand_in_db.id
            olog.log("ClarksTracker._set_brands << Brand <b>"+brand_in_db.name+"</b> already in database with id <b>" + str(brandid) + "</b>", "info")
                
        storebrand_in_db = session.query(orm.StoreBrand).filter_by(storeid=unicode(self.storeid)).filter_by(brandid=brandid).filter_by(gender=gender).first()
        if storebrand_in_db is None:
            storebrand = {'key': None, 'storeid' : None, 'brandid' : None, 'gender' : None, 'url' : None}
            sb = orm.StoreBrand(brand['key'], self.storeid, brandid, gender, brand['shopUrl'])
            olog.log("ClarksTracker._set_brands << Inserted <b>"+str(sb)+"</b>", "warning")
            if insert is True:
                session.add(sb)
                session.flush()
        else:
            olog.log("ClarksTracker._set_brands << StoreBrand <b>"+str(storebrand_in_db)+"</b> already in database with id <b>" + str(storebrand_in_db.id) + "</b>", "info")
            
        brands.append(br)
        
        if insert is True:
            session.commit()

        return brands

    #############################################################################
    # Function:         _set_items_for_brand
    # Input:            self, brandurl, session, insert
    # Output:           items
    # Goal:             
    # Targets:          <ul id="prod-list" class="">
    #                       <li class="product-list-item ">
    #                           <p>
    #                               <a href="/p/26107882" data-prodcategory='Herenlaarzen Originals' data-prodname='Desert Boot' data-ajax="false">
    #                                   <img src="//assets.clarksmcr.com/products/2/6/1/26107882_A_llt.jpg" class="thumb-image" alt="Desert Boot, Zwart, Herenlaarzen Originals" data-prodname="Desert Boot" data-productid="26107882" />
    #                               </a>
    #
    def _set_items_for_brand(self, brand, session, insert):
        items = []
        
        olog.log("ClarksTracker._get_items_for_brand > Calling <b>"+brand.url+"</b>", "info")
        # hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; nl-NL; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729);'}
        # req = urllib2.Request(brand.url, headers=hdr)
        
        display = Display(visible=0, size=(800, 600))
        display.start()
        browser = webdriver.Firefox()
        browser.get(brand.url)
       
        lastHeight = browser.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")
        while True:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print "Scrolling down..."
            time.sleep(10)
            newHeight = browser.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")
            if newHeight == lastHeight:
                break
            lastHeight = newHeight

        data = browser.page_source
        browser.quit()
        display.stop()
        
        try:
            tree = lxml.html.fromstring(data)
            all_items = tree.cssselect('ul[id*=\"prod-list\"] li[class*=\"product-list-item\"] p a[href*=\"\/p\/\"]')
            
            
            for it in all_items:
                if it is not None:
                    date = time.strftime('%Y-%m-%d %H:%M:%S')    
                    iid = it.attrib['href'].split('p/')[1]
                    i = session.query(orm.Item).filter_by(itemid=iid).filter_by(storeid=self.storeid).first()
                    if i is None:
                        item = self._get_item(brand, iid)
                        i = orm.Item(item['storeid'], item['itemid'], item['brandid'], item['link'], item['color'], item['title'], item['category'], item['gender'], item['uuid'])
                        olog.log("ClarksTracker._get_items_for_brand >>> Inserted item <b>"+str(i)+"</b>", "warning")
                        if insert is True:
                            session.add(i)
                            session.flush()
                            itemid = i.id
                        
                            for imageurl in item['images']:
                                ii = orm.ItemImage(itemid, imageurl)
                                olog.log("ClarksTracker._get_items_for_brand >>>> Inserted image <b>"+str(ii)+"</b>", "warning")
                                session.add(ii)
                            ip = orm.ItemPrice(itemid, item['price'], item['currency'], date)
                            olog.log("ClarksTracker._get_items_for_brand >>>> Inserted price <b>"+str(ip)+"</b>", "warning")
                            session.add(ip)
                    else:
                        itemid = i.id
                        olog.log("ClarksTracker._get_items_for_brand <<< <b>"+i.title+"</b> already in database with id <b>" + str(itemid) + "</b>", "info")
                    #endif i is None
                    items.append(i)
                #endif it is not None
            #endfor it in all_items
        except:
            pass # Opening url went wrong
        if insert is True:
            session.commit()
        #endif insert is True
        olog.log("ClarksTracker._get_items_for_brand < Found <b>"+str(len(items))+" products</b>", "info")
        
        return items
    
    def _get_item(self, brand, itemid):
        item = {'storeid' : None, 'itemid' : None, 'brandid' : None, 'link' : None, 'color' : None, 'title' : None, 'category' : None, 'gender' : None}
        item['storeid'] = self.storeid
        item['link'] = "http://www.clarks.nl/p/"+itemid
        item['brandid'] = brand.brandid
        item['itemid'] = itemid
        olog.log("ClarksTracker._get_products_for_brand >> Calling <b>"+item['link']+"</b>", "debug")

        hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; nl-NL; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729);'}
        req = urllib2.Request(item['link'], headers=hdr)
        idata = urllib2.urlopen(req).read()
        itree = lxml.html.fromstring(idata)
        
        item['images'] = self._get_images(idata, itree)
        item['price'] = self._get_price(itree)
        item['currency'] = self._get_currency(itree)
        item['color'] = self._get_color(itree)
        item['title'] = self._get_title(itree)
        item['category'] = self._get_category(itree)
        item['gender'] = brand.gender.title()
        item['uuid'] = str(shortuuid.uuid(item['link']))
        
        return item
    
    def _get_images(self, idata, itree):
        images = []
        try:
            image_data = itree.cssselect('div[id*=\"product-image\"] img[id*=\"main-image\"]')
            image_link = image_data[0].attrib['src']
            images.append(image_link)
            regexp = 'ImagePath'
            result = re.findall(regexp, idata)
            for i in range(2,len(result)):
                new_link = str.replace(image_link, '_A_', '_' + chr(64+i) +'_')
                images.append(new_link)
        except:
            pass
        return images
        
    def _get_price(self, itree):
        try:
            price_meta = itree.cssselect('input[id*=\'Price\']')
            price = price_meta[0].attrib['value'].replace(',', '.')
            return price
        except:
            return ""
        
    def _get_currency(self, itree):
        try:
            currency_meta = itree.cssselect('meta[itemprop*=\'priceCurrency\']')
            currency = currency_meta[0].attrib['content']
            return currency
        except:
            return ""

    def _get_color(self, itree):
        try:
    	    color_meta = itree.cssselect('span[class*=\'colour\']')
    	    color = unicode(color_meta[0].text_content()).encode('ascii', 'xmlcharrefreplace')
            return color
        except:
            return ""
        
    def _get_title(self, itree):
    	try:
    	    title_data = itree.cssselect('input[id*=\'ProductName\']')
    	    title = title_data[0].attrib['value']
    	    return title
    	except:
    	    return ""

    def _get_category(self, itree):    
        try:
            category_meta = itree.cssselect('span[class*=\'category\']')
            category = category_meta[0].text_content().strip()
            return category
        except:
            return ""
        