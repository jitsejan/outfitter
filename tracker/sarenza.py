################################################################################
# Application:      Outfitter
# File:             sarenza.py
# Goal:             
# Input:            
# Output:           
# Example:          
#
# History:          2016-02-12 - JJ     Creation of the file
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

class SarenzaTracker(Tracker):

    def __init__(self, *args, **kwargs):
        super(SarenzaTracker,self).__init__('Sarenza', *args, **kwargs)

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
        brands = []
            
        # Male
        maleBrandsUrl = "http://www.sarenza.nl/herenschoenen"
        gender = "male"
        olog.log("SarenzaTracker._set_brands > Calling <b>"+maleBrandsUrl+"</b>", 'info')
        
        display = Display(visible=0, size=(1920, 1080))
        display.start()
        browser = webdriver.Firefox()
        browser.get(maleBrandsUrl)
        data = browser.page_source
        
        tree = lxml.html.fromstring(data)
        
        brand_data = tree.cssselect('ul[class*=\"search-list\"] li a')
        for b in brand_data:
            brand = {'key' : None, 'name' : None, 'logoUrl' : None, 'logoLargeUrl' : None, 'shopUrl' : None}
            brand['name'] = unicode(b.text_content()).encode('ascii', 'xmlcharrefreplace')
            brandA = "http://sarenza.nl/Search.aspx?Ftq="+brand['name']+"%20dames"
            req = urllib2.Request(brandA.replace(' ', '%20'), headers=hdr)
            adata = urllib2.urlopen(req).read()
            atree = lxml.html.fromstring(adata)
            prod_data = atree.cssselect('ul[class*=\"vignettes\"] li a')
            prodUrl = prod_data[0].attrib['href']
            req = urllib2.Request(prodUrl, headers=hdr)
            bdata = urllib2.urlopen(req).read()
            btree = lxml.html.fromstring(bdata)
            brand['logoLargeUrl'] = btree.cssselect('img[id*=\"ImgBrandName\"]')[0].attrib['src'].split('?')[0]
            brand['shopUrl'] = "http://www.sarenza.nl"+b.attrib['href']
            
            regexp = 'Brand=([0-9]*)'
            result = re.search(regexp, brand['shopUrl'])
            if result:
                brand['key'] = result.group(1)
            
            uuid = str(shortuuid.uuid(brand['name']))
            br = orm.Brand(brand['name'], brand['logoUrl'], brand['logoLargeUrl'], uuid)

            brand_in_db = session.query(orm.Brand).filter_by(name=unicode(br.name)).first()
            if brand_in_db is None:
                olog.log("SarenzaTracker._set_brands <<< Inserted brand <b>"+br.name+"</b> with id <b>" + str(br.id) + "</b>", "warning")
                if insert is True:
                    session.add(br)
                    session.flush()
                    brandid = br.id
            else:
                brandid = brand_in_db.id
                olog.log("Brand <b>"+str(brand_in_db)+"</b> already in database with id <b>" + str(brandid) + "</b>", "info")
                
            storebrand_in_db = session.query(orm.StoreBrand).filter_by(storeid=unicode(self.storeid)).filter_by(brandid=brandid).filter_by(gender=gender).first()
            if storebrand_in_db is None:
                storebrand = {'key': None, 'storeid' : None, 'brandid' : None, 'gender': None, 'url' : None}
                sb = orm.StoreBrand(brand['key'], self.storeid, brandid, gender, brand['shopUrl'])
                olog.log("SarenzaTracker._set_brands <<< Inserted <b>"+str(sb)+"</b>", "warning")
                if insert is True:
                    session.add(sb)
                    session.flush()
            else:
                olog.log("SarenzaTracker._set_brands <<< <b>"+str(storebrand_in_db)+"</b> already in database", "info")
            brands.append(br)
        
        # Female
        femaleBrandsUrl = 'http://www.sarenza.nl/alle-damesschoenen'
        gender = "female"
        olog.log("SarenzaTracker._set_brands > Calling <b>"+femaleBrandsUrl+"</b>", 'info')
        
        browser.get(femaleBrandsUrl)
        data = browser.page_source
        browser.quit()
        display.stop()
        
        tree = lxml.html.fromstring(data)
        
        brand_data = tree.cssselect('ul[class*=\"search-list\"] li a')
        for b in brand_data:
            brand = {'key' : None, 'name' : None, 'logoUrl' : None, 'logoLargeUrl' : None}
            brand['name'] = unicode(b.text_content()).encode('ascii', 'xmlcharrefreplace').strip()
            brandA = "http://sarenza.nl/Search.aspx?Ftq="+brand['name']+"%20dames"
            req = urllib2.Request(brandA.replace(' ', '%20'), headers=hdr)
            adata = urllib2.urlopen(req).read()
            atree = lxml.html.fromstring(adata)
            prod_data = atree.cssselect('ul[class*=\"vignettes\"] li a')
            prodUrl = prod_data[0].attrib['href']
            req = urllib2.Request(prodUrl, headers=hdr)
            bdata = urllib2.urlopen(req).read()
            btree = lxml.html.fromstring(bdata)
            brand['logoLargeUrl'] = btree.cssselect('img[id*=\"ImgBrandName\"]')[0].attrib['src'].split('?')[0]
            brand['shopUrl'] = btree.cssselect('div[class*=\"row-fl\"] div[class*=\"item\"] a')[0].attrib['href']
            regexp = 'Brand=([0-9]*)'
            result = re.search(regexp, brand['shopUrl'])
            if result:
                brand['key'] = result.group(1)
                
            uuid = str(shortuuid.uuid(brand['name']))
            br = orm.Brand(brand['name'], brand['logoUrl'], brand['logoLargeUrl'], uuid)

            brand_in_db = session.query(orm.Brand).filter_by(name=unicode(br.name)).first()
            if brand_in_db is None:
                olog.log("SarenzaTracker._set_brands <<< Inserted brand <b>"+str(br)+"</b> with id <b>" + str(br.id) + "</b>", "warning")
                if insert is True:
                    session.add(br)
                    session.flush()
                    brandid = br.id
            else:
                brandid = brand_in_db.id
                olog.log("Brand <b>"+str(brand_in_db)+"</b> already in database with id <b>" + str(brandid) + "</b>", "info")
                
            storebrand_in_db = session.query(orm.StoreBrand).filter_by(storeid=unicode(self.storeid)).filter_by(brandid=brandid).filter_by(gender=gender).first()
            if storebrand_in_db is None:
                storebrand = {'key': None, 'storeid' : None, 'brandid' : None, 'gender': None, 'url' : None}
                sb = orm.StoreBrand(brand['key'], self.storeid, brandid, gender, brand['shopUrl'])
                olog.log("SarenzaTracker._set_brands <<< Inserted <b>"+str(sb)+"</b>", "warning")
                if insert is True:
                    session.add(sb)
                    session.flush()
            else:
                olog.log("SarenzaTracker._set_brands <<< <b>"+str(storebrand_in_db)+"</b> already in database", "info")

            brands.append(br)
        session.commit()

        return brands

    def _set_items_for_brand(self, brand, session, insert):
        global hdr
        items = []
        
        date = time.strftime('%Y-%m-%d %H:%M:%S')
        olog.log("SarenzaTracker._set_items_for_brand >>> Get articles <b>"+brand.url+"</b>", 'debug')
        try:
            req = urllib2.Request(brand.url, headers=hdr)
            data = urllib2.urlopen(req).read()
            tree = lxml.html.fromstring(data)
        
            # Find pagination
            base_url = brand.url.split('?')[0]
            pagination_data = tree.cssselect('footer[class*=\"pagination\"] span[class*=\"page\"] a')
            
            if len(pagination_data) > 1:
                for page in pagination_data:
                    items_data = tree.cssselect('ul[class*=\"vignettes\"] li[class*=\"slide vignette product\"] a')
                    for it in items_data:
                        if it.attrib['href'] is not '#':
                            iid = it.attrib['href'].split('-')[-1]
                            i = session.query(orm.Item).filter_by(itemid=iid).filter_by(storeid=self.storeid).first()
                            if i is None:
                                item = self._get_item(brand, it.attrib['href'])
                                i = orm.Item(item['storeid'], item['itemid'], item['brandid'], item['link'], item['color'], item['title'], item['category'], item['gender'], item['uuid'])
                                olog.log("SarenzaTracker._set_items_for_brand <<< Inserted item <b>"+str(i)+"</b>>", "warning")
                                if insert is True:
                                    session.add(i)
                                    session.flush()
                                    itemid = i.id
                                    for imageurl in item['images']:
                                        ii = orm.ItemImage(itemid, imageurl)
                                        olog.log("SarenzaTracker._sget_items_for_brand <<<< Inserted image <b>"+str(ii)+"</b>", "warning")
                                        if insert is True:     
                                            session.add(ii)
                                    ip = orm.ItemPrice(itemid, item['price'], item['currency'], date)
                                    olog.log("SarenzaTracker._set_items_for_brand <<<< Inserted price <b>"+str(ip)+"</b>", "warning")
                                    if insert is True:
                                        session.add(ip)                       
                                
                            else:
                                olog.log("SarenzaTracker._set_items_for_brand <<< <b>"+str(i)+"</b> already in database</b>", "info")
                            
                            items.append(i)
                            #endif i is None
                        #endif it.attrib['href'] is not '#'
                    #endfor it in items_data 
                    pageurl = base_url + page.attrib['data-url']
                    req = urllib2.Request(pageurl, headers=hdr)
                    data = urllib2.urlopen(req).read()
                    tree = lxml.html.fromstring(data)
                #endfor page in pagination_data
            else:
                items_data = tree.cssselect('ul[class*=\"vignettes\"] li[class*=\"slide vignette product\"] a')
                for it in items_data:
                    if it.attrib['href'] is not '#':
                        iid = it.attrib['href'].split('-')[-1]
                        i = session.query(orm.Item).filter_by(itemid=iid).filter_by(storeid=self.storeid).first()
                        if i is None:
                            item = self._get_item(brand, it.attrib['href'])
                            i = orm.Item(item['storeid'], item['itemid'], item['brandid'], item['link'], item['color'], item['title'], item['category'], item['gender'], item['uuid'])
                            olog.log("SarenzaTracker._set_items_for_brand <<< Inserted item <b>"+str(i)+"</b>>", "warning")
                            if insert is True:
                                session.add(i)
                                session.flush()
                                itemid = i.id
                                for imageurl in item['images']:
                                    ii = orm.ItemImage(itemid, imageurl)
                                    olog.log("SarenzaTracker._sget_items_for_brand <<<< Inserted image <b>"+str(ii)+"</b>", "warning")
                                    if insert is True:     
                                        session.add(ii)
                                ip = orm.ItemPrice(itemid, item['price'], item['currency'], date)
                                olog.log("SarenzaTracker._set_items_for_brand <<<< Inserted price <b>"+str(ip)+"</b>", "warning")
                                if insert is True:
                                    session.add(ip)                       
                            
                        else:
                            olog.log("SarenzaTracker._set_items_for_brand <<< <b>"+str(i)+"</b> already in database</b>", "info")
                        
                        items.append(i)
                        #endif i is None
                    #endif it.attrib['href'] is not '#'
                #endfor it in items_data      
                    
            
            if insert is True:
                session.commit()
        except:
            olog.log("SarenzaTracker._set_items_for_brand <<< Error opening URL", 'error')
            
        return items
        
    def _get_item(self, brand, url):
        global hdr
        item = {'storeid' : None, 'itemid' : None, 'brandid' : None, 'link' : None, 'color' : None, 'title' : None, 'category' : None, 'gender' : None}
        item['storeid'] = self.storeid
        item['link'] = url
        item['brandid'] = brand.brandid
        item['gender'] = brand.gender.title()
        item['itemid'] = item['link'].split('-')[-1]
        item['uuid'] = str(shortuuid.uuid(item['link']))
        olog.log("SarenzaTracker._get_item >> Calling <b>"+item['link']+"</b>", "debug")
        req = urllib2.Request(item['link'], headers=hdr)
        idata = urllib2.urlopen(req).read()
        itree = lxml.html.fromstring(idata)
        
        item['images'] = self._get_images(itree)
        item['price'] = self._get_price(itree)
        item['currency'] = self._get_currency(itree)
        item['color'] = self._get_color(itree)
        item['title'] = self._get_title(itree)
        item['category'] = self._get_category(idata)
        
        return item
    
    def _get_images(self, itree):
        images = []
        try:
            image_data = itree.cssselect('div[class*=\"product-view\"] div[class*=\"product-gallery\"] div[class*=\"iosSlider\"] div[class*=\"slider\"] div[class*=\"slide\"] img[itemprop*=\"image\"]')
            for image in image_data:
                image_link = image.attrib['src']
                images.append(image_link)
        except:
            pass
        
        return images
    
    def _get_price(self, itree):
        try:
            return itree.cssselect('span[class*=\'product-price\']')[0].text_content().strip().replace(',', '.')[1:]
        except:
            return ""
            
    def _get_currency(self, itree):
        try:
            return itree.cssselect('meta[itemprop*=\'priceCurrency\']')[0].attrib['content']
        except:
            return ""
    
    def _get_color(self, itree):
        try:
            color = itree.cssselect('h4[class*=\'color-placeholder\']')[0].text_content().strip()
            return unicode(color).encode('ascii', 'xmlcharrefreplace')
        except:
            return ""
        
    def _get_title(self, itree):
    	try:
    	    return itree.cssselect('span[itemprop*=\'name\']')[0].text_content().strip().encode('ascii', 'xmlcharrefreplace')
    	except:
    	    return ""
    	    
    def _get_category(self, idata):    
        try:
            regexp = '"prdparam-type_principal","(.*?)"'
            result = re.search(regexp, idata)
            return unicode(result.group(1))
        except:
            return ""
