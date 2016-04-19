################################################################################
# Application:      Outfitter
# File:             bijenkorf.py
# Goal:             
# Input:            
# Output:           
# Example:          
#
# History:          2016-02-25 - JJ     Creation of the file
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
from datetime import datetime

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

class BijenkorfTracker(Tracker):

    def __init__(self, *args, **kwargs):
        super(BijenkorfTracker,self).__init__('Bijenkorf', *args, **kwargs)

    #############################################################################
    # Function:         _get_brands
    # Input:            
    # Output:           
    # Goal:             
    # Targets:           <ul class="search-list" data-facet-id="2">
    #                      <li>
    #                           <a href="/HomeFh.aspx?Brand=4&amp;multigender=2" class="eatrckr" data-ea="Marques - Adidas Originals"><span>Adidas Originals</span></a>
    #                       </li>
    def _set_brands(self, session, insert):
        global hdr
        brands = []
        urls['male']  = "http://www.debijenkorf.nl/merken/herenmode"
        urls['female'] = "http://www.debijenkorf.nl/merken/damesmode"
        
        for gender, url in enumerate(urls):
            olog.log("BijenkorfTracker._set_brands > Calling <b>"+url+"</b>", 'info')
            
            req = urllib2.Request(url, headers=hdr)
            data = urllib2.urlopen(req).read()
            tree = lxml.html.fromstring(data)
            brand_data = tree.cssselect('div[class*=\"brands-block-list\"] ul[class*=\"col\"] li a')
            for b in brand_data:
                brand = {'key' : None, 'name' : None, 'logoUrl' : None, 'logoLargeUrl' : None, 'shopUrl' : None}
                burl = 'http://www.debijenkorf.nl'+b.attrib['href']
                breq = urllib2.Request(burl, headers=hdr)
                bdata = urllib2.urlopen(breq).read()
                btree = lxml.html.fromstring(bdata)             
                brand['name'] = unicode(b.text_content().title()).encode('ascii', 'xmlcharrefreplace')
                try: # More than 24 items per page
                    br_data = btree.cssselect('a[class*=\"dbk-productlist-summary--link\"]')
                    brand['shopUrl'] = br_data[1].attrib['data-href']
                except: # Less than 24 items for this brand
                    brand['shopUrl'] = burl
    
                brand_in_db = session.query(orm.Brand).filter_by(name=unicode(brand['name'])).first()
                if brand_in_db is None:
                    uuid = str(shortuuid.uuid(brand['name']))
                    br = orm.Brand(brand['name'], brand['logoUrl'], brand['logoLargeUrl'], uuid)
                    olog.log("BijenkorfTracker._set_brands <<< Inserted brand <b>"+str(br)+"</b> with id <b>" + str(br.id) + "</b>", "warning")
                    if insert is True:
                        session.add(br)
                        session.flush()
                        brandid = br.id
                else:
                    br = brand_in_db
                    olog.log("BijenkorfTracker._set_brands <<< Brand <b>"+str(brand_in_db)+"</b> already in database", "info")                
                    brandid = brand_in_db.id
    
                  
                storebrand_in_db = session.query(orm.StoreBrand).filter_by(storeid=unicode(self.storeid)).filter_by(brandid=brandid).filter_by(gender=gender).first()
                
                if storebrand_in_db is None:
                    storebrand = {'key': None, 'storeid' : None, 'brandid' : None, 'gender': None, 'url' : None}
                    sb = orm.StoreBrand(brand['key'], self.storeid, brandid, gender, brand['shopUrl'])
                    olog.log("BijenkorfTracker._set_brands <<< Inserted <b>"+str(sb)+"</b>", "warning")
                    if insert is True:
                        session.add(sb)
                        session.flush()
                else:
                    olog.log("BijenkorfTracker._set_brands <<< <b>"+str(storebrand_in_db)+"</b> already in database", "info")
                brands.append(br)
            # endfor brand_data
        # endfor enumerate(urls)
        
        session.commit()

        return brands

    def _get_items_for_brand(self, brand, session, insert, thisweekonly = False):
        global hdr
        items = []
        num_items = 0
        date = time.strftime('%Y-%m-%d')
        olog.log("BijenkorfTracker._set_items_for_brand >>> Get articles <b>"+brand.url+"</b>", 'debug')
        
        if thisweekonly is True:
            brand.url += '%7d%2fnieuw_nonfashion%3E%7bnet20binnen'
        
        try:
            req = urllib2.Request(brand.url, headers=hdr)
            data = urllib2.urlopen(req).read()
            tree = lxml.html.fromstring(data)
        
            items_data = tree.cssselect('li[class*=\"dbk-productlist-thumbnail\"] a[itemprop*=\"url\"]')
            for it in items_data:
                iid = it.attrib['href'].split('-')[-1]
                i = session.query(orm.Item).filter_by(itemid=iid).filter_by(storeid=self.storeid).first()
                item = self._get_item(brand, it.attrib['href'])
                if i is None:
                    i = orm.Item(item['storeid'], item['itemid'], item['brandid'], item['link'], item['color'], item['title'], item['category'], item['gender'], item['uuid'])
                    olog.log("BijenkorfTracker._set_items_for_brand <<< Inserted item <b>"+str(i)+"</b>>", "warning")
                    if insert is True:
                        session.add(i)
                        session.flush()
                        itemid = i.id
                        num_items += 1
                        
                        for imageurl in item['images']:
                            ii = session.query(orm.ItemImage).filter_by(itemid=itemid).filter_by(imageurl=imageurl).first()
                            if ii is not None:
                                olog.log("BijenkorfTracker._set_items_for_brand <<<< <b>"+str(ii)+"</b> already in database</b>", "info")
                            else:
                                ii = orm.ItemImage(itemid, imageurl)
                                olog.log("BijenkorfTracker._set_items_for_brand <<<< Inserted image <b>"+str(ii)+"</b>", "warning")
                                session.add(ii)
                        
                        ip = session.query(orm.ItemPrice).filter_by(itemid=itemid).filter_by(checkdate=date).first()
                        if ip is not None:
                            olog.log("BijenkorfTracker._set_items_for_brand <<< <b>"+str(ip)+"</b> already in database</b>", "info")
                        else:
                            ip = orm.ItemPrice(itemid, item['price'], item['currency'], date)
                            olog.log("BijenkorfTracker._set_items_for_brand <<<< Inserted price <b>"+str(ip)+"</b>", "warning")
                            session.add(ip)       
                else:
                    olog.log("BijenkorfTracker._set_items_for_brand <<< <b>"+str(i)+"</b> already in database</b>", "info")
                    itemid = i.id
                #endif i is None
                
                                
            
                items.append(i)
            #endfor it in items_data 
    
            # Find pagination
            pagination_data = tree.cssselect('ul[class*=\"dbk-pagination\"] li a')
            if len(pagination_data) > 1:
                for page in pagination_data[1:-1]:
                    sreq = urllib2.Request(page.attrib['data-href'], headers=hdr)
                    sdata = urllib2.urlopen(sreq).read()
                    stree = lxml.html.fromstring(sdata)
                    items_data = stree.cssselect('li[class*=\"dbk-productlist-thumbnail\"] a[itemprop*=\"url\"]')
                    for it in items_data:
                        iid = it.attrib['href'].split('-')[-1]
                        i = session.query(orm.Item).filter_by(itemid=iid).filter_by(storeid=self.storeid).first()
                        item = self._get_item(brand, it.attrib['href'])
                        if i is None:
                            i = orm.Item(item['storeid'], item['itemid'], item['brandid'], item['link'], item['color'], item['title'], item['category'], item['gender'], item['uuid'])
                            olog.log("BijenkorfTracker._set_items_for_brand <<< Inserted item <b>"+str(i)+"</b>>", "warning")
                            if insert is True:
                                session.add(i)
                                session.flush()
                                itemid = i.id
                                num_items += 1
                            for imageurl in item['images']:
                                ii = session.query(orm.ItemImage).filter_by(itemid=itemid).filter_by(imageurl=imageurl).first()
                                if ii is not None:
                                    olog.log("BijenkorfTracker._set_items_for_brand <<<< <b>"+str(ii)+"</b> already in database</b>", "info")
                                else:
                                    ii = orm.ItemImage(itemid, imageurl)
                                    olog.log("BijenkorfTracker._set_items_for_brand <<<< Inserted image <b>"+str(ii)+"</b>", "warning")
                                    if insert is True:     
                                        session.add(ii)
                            
                            ip = session.query(orm.ItemPrice).filter_by(itemid=itemid).filter_by(checkdate=date).first()
                            if ip is not None:
                                olog.log("BijenkorfTracker._set_items_for_brand <<< <b>"+str(ip)+"</b> already in database</b>", "info")
                            else:
                                ip = orm.ItemPrice(itemid, item['price'], item['currency'], date)
                                olog.log("BijenkorfTracker._set_items_for_brand <<<< Inserted price <b>"+str(ip)+"</b>", "warning")
                                if insert is True:
                                    session.add(ip) 
                        else:
                            olog.log("BijenkorfTracker._set_items_for_brand <<< <b>"+str(i)+"</b> already in database</b>", "info")
                            itemid = i.id
                        #endif i is None
                                              
                    
                        items.append(i)
                    #endfor it in items_data 
                #endfor page in pagination_data
            if insert is True:
                session.commit()
        except:
            olog.log("BijenkorfTracker._set_items_for_brand <<< Error opening URL", 'error')
            
        return num_items
        
    def _get_item(self, brand, url):
        global hdr
        item = {'storeid' : None, 'itemid' : None, 'brandid' : None, 'link' : None, 'color' : None, 'title' : None, 'category' : None, 'gender' : None}
        item['storeid'] = self.storeid
        if 'debijenkorf.nl' not in url:
            url = 'http://debijenkorf.nl'+url
        item['link'] = url
        item['brandid'] = brand.brandid
        item['gender'] = brand.gender.title()
        item['itemid'] = item['link'].split('-')[-1]
        item['uuid'] = str(shortuuid.uuid(item['link']))
        olog.log("BijenkorfTracker._get_item >> Calling <b>"+item['link']+"</b>", "debug")
        req = urllib2.Request(item['link'], headers=hdr)
        idata = urllib2.urlopen(req).read()
        itree = lxml.html.fromstring(idata)
        
        item['images'] = self._get_images(itree)
        item['price'] = self._get_price(idata)
        item['currency'] = self._get_currency(itree)
        item['color'] = self._get_color(itree)
        item['title'] = self._get_title(idata)
        item['category'] = self._get_category(idata)
        
        return item
    
    def _get_images(self, itree):
        images = []
        try:
            image_data = itree.cssselect('img[data-dbk-target-selector*=\"main-image\"]')
            for image in image_data:
                try:
                    images.append(image.attrib['data-dbk-target-src'])
                except:
                    pass # false positive
            # Return the links to the images
            if len(images) < 1:
                try:
                    images.append(itree.cssselect('img[class*=\"main-image\"]')[0].attrib['src'])
                except:
                    pass
        except:
            pass
        return images
    
    def _get_price(self, idata):
        try:
            return re.search('"price": "(.*)?"', idata).group(1)
        except:
            return ""
    
    def _get_currency(self, itree):
        try:
            return itree.cssselect('meta[itemprop*=\'priceCurrency\']')[0].attrib['content']
        except:
            return ""
    
    def _get_color(self, itree):
        try:
            return unicode(itree.cssselect('span[itemprop*=\'color\']')[0].text_content()).encode('ascii', 'xmlcharrefreplace')
        except:
            return ""
        
    def _get_title(self, idata):
        try:
            regexp = '"name": "(.*)?"'
            result = re.search(regexp, idata)
            return unicode(result.group(1)).encode('ascii', 'xmlcharrefreplace')
        except:
            return ""
    
    def _get_category(self, idata):    
        try:
            return re.search('"category": "(.*)?"', idata).group(1).split('/')[-1]
        except:
            return ""      

    def _get_new_items(self, session):
        tot_num_items = 0
        start = datetime.now()
        for storebrand in self._brands:
            num_items = self._get_items_for_brand(storebrand[0], session, insert=True, thisweekonly=True)
            tot_num_items += num_items
        end = datetime.now()
        olog.log("BijenkorfTracker._get_new_items < Added <b>"+str(tot_num_items)+"</b> new items in "+ str(end-start) +"!", 'info')