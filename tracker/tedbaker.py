# -*- coding: utf-8 -*-
################################################################################
# Application:      Outfitter
# File:             tedbaker.py
# Goal:             
# Input:            
# Output:           
# Example:          
#
# History:          2016-02-19 - JJ     Creation of the file
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

################################################################################
# Definitions
################################################################################
author =    "JJ"
appName =   "Outfitter"
hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; nl-NL; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729);'}

################################################################################
# Functions
################################################################################

################################################################################
# Classes
################################################################################

class TedBakerTracker(Tracker):

    def __init__(self, *args, **kwargs):
        super(TedBakerTracker,self).__init__('Ted Baker', *args, **kwargs)

    ############################################################################
    # Function:         _get_brands
    # Input:            self, session, insert
    # Output:           brands
    # Goal:             
    # Targets:          <div id="brands_section">
    #                       <div id="letter_a" class="letter">
    #                           <h2>A</h2>
    #                           <ul><!--mp_trans_remove_start-->
    #                               <li><a href="http://www.asos.com/men/a-to-z-of-brands/abercrombie-and-fitch/cat/?cid=19971"><strong>Abercrombie &amp; Fitch</strong></a></li>
    #
    # 
    def _set_brands(self, session, insert):
        brands = []
        
        brand = {'key' : None, 'name' : None, 'logoUrl' : None, 'logoLargeUrl' : None, 'shopUrl' : None}
        brand['name'] = 'Ted Baker' # Fixed. Website only sells Ted Baker
        brand['shopUrl'] = 'http://www.tedbaker.com/nl/Mens/c/category_mens'
        uuid = str(shortuuid.uuid(brand['name']))
        gender = 'Male'
        br = orm.Brand(brand['name'], brand['logoUrl'], brand['logoLargeUrl'], uuid)
        olog.log("TedBakerTracker._set_brands << Found brand <b>"+str(br)+"</b>", 'debug')

        brand_in_db = session.query(orm.Brand).filter_by(name=unicode(br.name)).first()
        if brand_in_db is None:
            if insert is True:
                session.add(br)
                session.flush()
                brandid = br.id
                olog.log("TedBakerTracker._set_brands >>> Inserted brand <b>"+br.name+"</b> with id <b>" + str(brandid) + "</b>", "warning")
        else:
            brandid = brand_in_db.id
            olog.log("TedBakerTracker._set_brands << Brand <b>"+brand_in_db.name+"</b> already in database with id <b>" + str(brandid) + "</b>", "info")
                
        storebrand_in_db = session.query(orm.StoreBrand).filter_by(storeid=unicode(self.storeid)).filter_by(brandid=brandid).filter_by(gender=gender).first()
        if storebrand_in_db is None:
            storebrand = {'key': None, 'storeid' : None, 'brandid' : None, 'gender' : None, 'url' : None}
            sb = orm.StoreBrand(brand['key'], self.storeid, brandid, gender, brand['shopUrl'])
            olog.log("TedBakerTracker._set_brands << Inserted <b>"+str(sb)+"</b>", "warning")
            if insert is True:
                session.add(sb)
                session.flush()
        else:
            olog.log("TedBakerTracker._set_brands << StoreBrand <b>"+str(storebrand_in_db)+"</b> already in database with id <b>" + str(storebrand_in_db.id) + "</b>", "info")
            
        brands.append(br)

        brand = {'key' : None, 'name' : None, 'logoUrl' : None, 'logoLargeUrl' : None, 'shopUrl' : None}
        brand['name'] = 'Ted Baker' # Fixed. Website only sells Clarks
        brand['shopUrl'] = 'http://www.tedbaker.com/nl/Womens/c/category_womens'
        uuid = str(shortuuid.uuid(brand['name']))
        gender = 'Female'
        br = orm.Brand(brand['name'], brand['logoUrl'], brand['logoLargeUrl'], uuid)
        olog.log("TedBakerTracker._set_brands << Found brand <b>"+str(br)+"</b>", 'debug')

        brand_in_db = session.query(orm.Brand).filter_by(name=unicode(br.name)).first()
        if brand_in_db is None:
            if insert is True:
                session.add(br)
                session.flush()
                brandid = br.id
                olog.log("TedBakerTracker._set_brands >>> Inserted brand <b>"+br.name+"</b> with id <b>" + str(brandid) + "</b>", "warning")
        else:
            brandid = brand_in_db.id
            olog.log("TedBakerTracker._set_brands << Brand <b>"+brand_in_db.name+"</b> already in database with id <b>" + str(brandid) + "</b>", "info")
                
        storebrand_in_db = session.query(orm.StoreBrand).filter_by(storeid=unicode(self.storeid)).filter_by(brandid=brandid).filter_by(gender=gender).first()
        if storebrand_in_db is None:
            storebrand = {'key': None, 'storeid' : None, 'brandid' : None, 'gender' : None, 'url' : None}
            sb = orm.StoreBrand(brand['key'], self.storeid, brandid, gender, brand['shopUrl'])
            olog.log("TedBakerTracker._set_brands << Inserted <b>"+str(sb)+"</b>", "warning")
            if insert is True:
                session.add(sb)
                session.flush()
        else:
            olog.log("TedBakerTracker._set_brands << StoreBrand <b>"+str(storebrand_in_db)+"</b> already in database with id <b>" + str(storebrand_in_db.id) + "</b>", "info")
            
        brands.append(br)
        
        if insert is True:
            session.commit()

        return brands

    #############################################################################
    # Function:         _set_items_for_brand
    # Input:            self, brandurl, session, insert
    # Output:           items
    # Goal:             
    # Targets:          
    #
    def _set_items_for_brand(self, brand, session, insert):
        global hdr
        items = []
        olog.log("TedBakerTracker._set_items_for_brand > Calling <b>"+brand.url+"</b>", "info")
        req = urllib2.Request(brand.url, headers=hdr)
        try:
            data = urllib2.urlopen(req).read()
            tree = lxml.html.fromstring(data)
            
            date = time.strftime('%Y-%m-%d')
            
            if 'women' in brand.url:
                section = '/Womens/'
            else:
                section = '/Mens/'
            
            pages_data = tree.cssselect('li[class=\"nav_item\"] a')
            for page in pages_data:
                if section in page.attrib['href']:
                    pageurl = 'http://www.tedbaker.com'+page.attrib['href']
                    olog.log("TedBakerTracker._set_items_for_brand >> Calling <b>"+pageurl+"</b>", "info")

                    preq = urllib2.Request(pageurl, headers=hdr)
                    pdata = urllib2.urlopen(preq).read()
                    ptree = lxml.html.fromstring(pdata)
                    all_items = ptree.cssselect('div[class*=\"product_list\"] div[class*=\"product-wrap\"] article div[class*=\"image\"] a[class*=\"image\"]')
                    for it in all_items:
                        iid = it.attrib['href'].split('/')[-1].split('-')[0]
                        i = session.query(orm.Item).filter_by(itemid=iid).filter_by(storeid=self.storeid).first()
                        item = self._get_item(brand, it.attrib['href'])
                        
                        if i is None:
                            i = orm.Item(item['storeid'], item['itemid'], item['brandid'], item['link'], item['color'], item['title'], item['category'], item['gender'], item['uuid'])
                            olog.log("TedBakerTracker._set_items_for_brand <<< Inserted item <b>"+str(i)+"</b>>", "warning")
                            if insert is True:
                                session.add(i)
                                session.flush()
                                itemid = i.id
                        else:
                            olog.log("TedBakerTracker._set_items_for_brand <<< <b>"+str(i)+"</b> already in database</b>", "info")
                            itemid = i.id
                        #endif i is None
                        
                        for imageurl in item['images']:
                            ii = session.query(orm.ItemImage).filter_by(itemid=itemid).filter_by(imageurl=imageurl).first()
                            if ii is not None:
                                olog.log("TedBakerTracker._set_items_for_brand <<<< <b>"+str(ii)+"</b> already in database</b>", "info")
                            else:
                                ii = orm.ItemImage(itemid, imageurl)
                                olog.log("TedBakerTracker._set_items_for_brand <<<< Inserted image <b>"+str(ii)+"</b>", "warning")
                                if insert is True:     
                                    session.add(ii)
                        
                        ip = session.query(orm.ItemPrice).filter_by(itemid=itemid).filter_by(checkdate=date).first()
                        if ip is not None:
                            olog.log("TedBakerTracker._set_items_for_brand <<< <b>"+str(ip)+"</b> already in database</b>", "info")
                        else:
                            ip = orm.ItemPrice(itemid, item['price'], item['currency'], date)
                            olog.log("TedBakerTracker._set_items_for_brand <<<< Inserted price <b>"+str(ip)+"</b>", "warning")
                            if insert is True:
                                session.add(ip)
                        items.append(i)
                     #endfor it in items_data 
                #endif section
            #endfor page in page_data
        except:
            olog.log("TedBakerTracker._set_items_for_brand <<< Error opening URL", 'error')

        
        if insert is True:
            session.commit()
        
        return items
    
    def _get_item(self, brand, itemurl):
        global hdr
        item = {'storeid' : None, 'itemid' : None, 'brandid' : None, 'link' : None, 'color' : None, 'title' : None, 'category' : None, 'gender' : None}
        item['storeid'] = self.storeid
        item['link'] = 'http://www.tedbaker.com'+itemurl
        item['brandid'] = brand.brandid
        item['itemid'] = item['link'].split('/')[-1].split('-')[0]
        
        olog.log("TedBakerTracker._get_item >> Calling <b>"+item['link']+"</b>", "debug")

        req = urllib2.Request(item['link'], headers=hdr)
        idata = urllib2.urlopen(req).read()
        itree = lxml.html.fromstring(idata)
        
        item['images'] = self._get_images(itree)
        item['price'] = self._get_price(itree)
        item['currency'] = self._get_currency(idata)
        item['color'] = self._get_color(itree)
        item['title'] = self._get_title(itree)
        item['category'] = self._get_category(idata)
        item['gender'] = brand.gender.title()
        item['uuid'] = str(shortuuid.uuid(item['link']))

        return item
    
    def _get_images(self, itree):
        images = []
        try:
            image_data = itree.cssselect('section[id*=\"product_images\"] div[class*=\"carousel\"] div[class*=\"frame\"] div[class*=\"viewport\"] div[class*=\"slider\"] div[class*=\"image\"] a img')
            for img in image_data:
                image = img.attrib['ng-src']
                image = image.replace("{{imageFormat[view.imgSizes]['pdp_primary']}}", "w=460%26h=575%26q=85") 
                if image not in images:
                    images.append(image)
        except:
            pass
        return images
        
    def _get_price(self, itree):
        try:
            return itree.cssselect('header[id*=\'product_head\'] ul[class*=\'pricing\'] li[class*=\'price\']')[0].text_content().strip()[2:]
        except:
            return ""
        
    def _get_color(self, itree):
        try:
            return unicode(itree.cssselect('div[class*=\'colours_switch\'] div[class*=\'frame\'] ul li[class*=\'selected\'] span[class*=\'image\']')[0].attrib['title']).encode('ascii', 'xmlcharrefreplace')
        except:
            return ""
        
    def _get_title(self, itree):
    	try:
    	    title = itree.cssselect('header[id*=\'product_head\'] hgroup h1[class*=\'name\']')[0].text_content().strip()
    	    description = itree.cssselect('header[id*=\'product_head\'] hgroup h2[class*=\'summary\']')[0].text_content().strip()
    	    title += ' - ' + description
    	    return unicode(title).encode('ascii', 'xmlcharrefreplace')
    	except:
    	    return ""

    def _get_category(self, idata):    
        try:
            return re.search('product_category : "(.*?)",', idata).group(1)
        except:
            return ""  

    def _get_currency(self, idata):    
        try:
            return re.search('site_currency : "(.*?)",', idata).group(1)
        except:
            return ""
