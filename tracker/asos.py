# -*- coding: utf-8 -*-
################################################################################
# Application:      Outfitter
# File:             asos.py
# Goal:             
# Input:            
# Output:           
# Example:          
#
# History:          2016-02-10 - JJ     Creation of the file
#
################################################################################

################################################################################
# Imports
################################################################################
from tracker import Tracker
from stores import asos
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

################################################################################
# Functions
################################################################################

################################################################################
# Classes
################################################################################

class AsosTracker(Tracker):

    def __init__(self, *args, **kwargs):
        super(AsosTracker,self).__init__('Asos', *args, **kwargs)

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
        
        maleBrandsUrl = "http://www.asos.com/men/a-to-z-of-brands/cat/pgehtml.aspx?cid=1361"
        gender = 'male'
        olog.log("AsosTracker._set_brands > Calling <b>"+maleBrandsUrl+"</b>", 'info')

        hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729); nl-NL'}
        req = urllib2.Request(maleBrandsUrl, headers=hdr)
        data = urllib2.urlopen(req).read()
        tree = lxml.html.fromstring(data)
        
        brand_data = tree.cssselect('div[id*=\"brands_section\"] div ul li a')
        for b in brand_data:
            brand = {'key' : None, 'name' : None, 'logoUrl' : None, 'logoLargeUrl' : None, 'shopUrl' : None}
            brand['name'] = unicode(b.text_content()).encode('ascii', 'xmlcharrefreplace')
            brand['shopUrl'] = b.attrib['href']
            brand['key'] = b.attrib['href'].rsplit('=',1)[1]
            uuid = str(shortuuid.uuid(brand['name']))
            br = orm.Brand(brand['name'], brand['logoUrl'], brand['logoLargeUrl'], uuid)
            olog.log("AsosTracker._set_brands << Found brand <b>"+br.name+"</b>", 'debug')

            if insert is True:
                brand_in_db = session.query(orm.Brand).filter_by(name=unicode(br.name)).first()
                if brand_in_db is None:
                    session.add(br)
                    session.flush()
                    brandid = br.id
                    olog.log("AsosTracker._set_brands >>> Inserted brand <b>"+br.name+"</b> with id <b>" + str(brandid) + "</b>", "warning")
                else:
                    brandid = brand_in_db.id
                    olog.log("Brand <b>"+brand_in_db.name+"</b> already in database with id <b>" + str(brandid) + "</b>", "debug")
                
                storebrand_in_db = session.query(orm.StoreBrand).filter_by(storeid=unicode(self.storeid)).filter_by(brandid=brandid).filter_by(gender=gender).first()
                if storebrand_in_db is None:
                    storebrand = {'key': None, 'storeid' : None, 'brandid' : None, 'gender' : None, 'url' : None}
                    sb = orm.StoreBrand(brand['key'], self.storeid, brandid, gender, brand['shopUrl'])
                    olog.log("AsosTracker._set_brands >>> Inserted <b>"+str(sb)+"</b>", "warning")
                    session.add(sb)
                    session.flush()


            brands.append(br)
        

        femaleBrandsUrl = "http://www.asos.com/Women/A-To-Z-Of-Brands/Cat/pgehtml.aspx?cid=1340"
        gender = 'female'
        olog.log("AsosTracker._set_brands > Calling <b>"+femaleBrandsUrl+"</b>", 'info')

        hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729); nl-NL'}
        req = urllib2.Request(femaleBrandsUrl, headers=hdr)
        data = urllib2.urlopen(req).read()
        tree = lxml.html.fromstring(data)
        
        brand_data = tree.cssselect('div[id*=\"brands_section\"] div ul li a')
        for b in brand_data:
            brand = {'key' : None, 'name' : None, 'logoUrl' : None, 'logoLargeUrl' : None, 'shopUrl' : None}
            brand['name'] = unicode(b.text_content()).encode('ascii', 'xmlcharrefreplace')
            brand['shopUrl'] = b.attrib['href']
            brand['key'] = b.attrib['href'].rsplit('=',1)[1]
            uuid = str(shortuuid.uuid(brand['name']))
            br = orm.Brand(brand['name'], brand['logoUrl'], brand['logoLargeUrl'], uuid)
            olog.log("AsosTracker._set_brands << Found brand <b>"+br.name+"</b>", 'debug')

            if insert is True:
                brand_in_db = session.query(orm.Brand).filter_by(name=unicode(br.name)).first()
                if brand_in_db is None:
                    session.add(br)
                    session.flush()
                    brandid = br.id
                    olog.log("AsosTracker._set_brands >>> Inserted brand <b>"+br.name+"</b> with id <b>" + str(brandid) + "</b>", "warning")
                else:
                    brandid = brand_in_db.id
                    olog.log("Brand <b>"+brand_in_db.name+"</b> already in database with id <b>" + str(brandid) + "</b>", "debug")
                
                storebrand_in_db = session.query(orm.StoreBrand).filter_by(storeid=unicode(self.storeid)).filter_by(brandid=brandid).filter_by(gender=gender).first()
                if storebrand_in_db is None:
                    storebrand = {'key': None, 'storeid' : None, 'brandid' : None, 'gender' : None, 'url' : None}
                    sb = orm.StoreBrand(brand['key'], self.storeid, brandid, gender, brand['shopUrl'])
                    olog.log("AsosTracker._set_brands >>> Inserted <b>"+str(sb)+"</b>", "warning")
                    session.add(sb)
                    session.flush()

            session.commit()
            brands.append(br)
        return brands

    #############################################################################
    # Function:         _get_items_for_brand
    # Input:            self, brandurl, session, insert
    # Output:           items
    # Goal:             
    # Targets:          <div id="items-wrapper" class="items">
    #            			<ul id="items">
    # 						    <li>
    # 						        <div class="categoryImageDiv" data-parentsku="">
    #                                   <a id="ctl00_ContentMainPage_ctlCategoryRefine_rptCategory_ctl00_hlproductImageLink" class="productImageLink" title="Nixon Silver Queenpin Watch" href="/Nixon/Nixon-Silver-Queenpin-Watch/Prod/pgeproduct.aspx?iid=5748476&amp;cid=8013&amp;sh=0&amp;pge=0&amp;pgesize=36&amp;sort=-1&amp;clr=Silver&amp;totalstyles=18&amp;gridsize=3"><img id="ctl00_ContentMainPage_ctlCategoryRefine_rptCategory_ctl00_imgProductImage" class="product-image" onload="crp.fire()" src="http://images.asos-media.com/inv/media/6/7/4/8/5748476/silver/image1xl.jpg" alt="Nixon Silver Queenpin Watch" style="border-width:0px;" /></a>
    def _get_items_for_brand(self, brand, session, insert):
        items = []
        olog.log("AsosTracker._get_items_for_brand > Calling <b>"+brand.url+"</b>", "info")
        hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; nl-NL; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729);'}
        req = urllib2.Request(brand.url, headers=hdr)
        try:
            data = urllib2.urlopen(req).read()
            tree = lxml.html.fromstring(data)
            
            date = time.strftime('%Y-%m-%d %H:%M:%S')
            
            all_items = tree.cssselect('div[id*=\"items-wrapper\"] ul[id*=\"items\"] li div[class*=\"categoryImageDiv\"] a[class*=\"productImageLink\"]')
            for it in all_items:
                if it is not None:
                    iid = it.attrib['href'].split('&')[0].split('=')[1]
                    if insert is True:
                        i = session.query(orm.Item).filter_by(itemid=iid).filter_by(storeid=self.storeid).first()
                        if i is None:
                            item = self._get_item(brand, it.attrib['href'].split('&')[0])
                            i = orm.Item(item['storeid'], item['itemid'], item['brandid'], item['link'], item['color'], item['title'], item['category'], item['gender'], item['uuid'])
                            session.add(i)
                            session.flush()
                            itemid = i.id
                            olog.log("AsosTracker._get_items_for_brand >>> Inserted item <b>"+str(i)+"</b> with id <b>" + str(itemid) + "</b>", "warning")
                            for imageurl in item['images']:
                                ii = orm.ItemImage(itemid, imageurl)
                                olog.log("AsosTracker._get_items_for_brand >>>> Inserted image <b>"+str(ii)+"</b>", "warning")
                                session.add(ii)
                            ip = orm.ItemPrice(itemid, item['price'], item['currency'], date)
                            olog.log("AsosTracker._get_items_for_brand >>>> Inserted price <b>"+str(ip)+"</b>", "warning")
                            session.add(ip)
                        else:
                            itemid = i.id
                            olog.log("AsosTracker._get_items_for_brand >>> <b>"+i.title+"</b> already in database with id <b>" + str(itemid) + "</b>", "warning")
                        #endif i is None
                    #endif insert is True    
                    items.append(i)
                #endif it is not None
            #endfor it in all_items
        except:
            pass # Opening url went wrong
        session.commit()
        
        olog.log("AsosTracker._get_items_for_brand < Found <b>"+str(len(items))+" products</b>", "info")
        
        return items
    
    def _get_item(self, brand, itemurl):
        item = {'storeid' : None, 'itemid' : None, 'brandid' : None, 'link' : None, 'color' : None, 'title' : None, 'category' : None, 'gender' : None}
        item['storeid'] = self.storeid
        item['link'] = "http://www.asos.com"+itemurl
        item['brandid'] = brand.id
        item['itemid'] = item['link'].split('=')[1]
        
        olog.log("AsosTracker._get_products_for_brand >> Calling <b>"+item['link']+"</b>", "debug")

        hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; nl-NL; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729);'}
        req = urllib2.Request(item['link'], headers=hdr)
        idata = urllib2.urlopen(req).read()
        itree = lxml.html.fromstring(idata)
        
        item['images'] = self._get_images(itree)
        item['price'] = self._get_price(item['link'])
        item['currency'] = self._get_currency(item['link'])
        item['color'] = self._get_color(itree, item['images'][0])
        item['title'] = self._get_title(itree)
        item['category'] = self._get_category(itree)
        item['gender'] = brand.gender.title()
        item['uuid'] = str(shortuuid.uuid(item['link']))
        
        return item
    
    def _get_images(self, itree):
        images = []
        try:
            image_data = itree.cssselect('div[id*=\"productImages\"] div[class*=\"productImagesItems\"] div[class*=\"image\"] img')
            for image in image_data:
                try:
                    images.append(image.attrib['src'])
                except:
                    pass # false positive
        except:
            pass
        return images
        
    def _get_price(self, url):
        hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; it; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729);'}
        url = url.replace('.com/', '.com/it/')
        req = urllib2.Request(url, headers=hdr)
        idata = urllib2.urlopen(req).read()
        try:
            regexp = '"ProductPriceInNetworkCurrency":"(.*?)"'
            result = re.search(regexp, idata)
            price = result.group(1)
        except:
            price = ""
        return price

    def _get_currency(self, url):
        currency = 'EUR' # Cheat, since for the price we pick the EUR version
        return currency
        
    def _get_color(self, itree, image):
        try:
            color = itree.cssselect('div[class*=\'colour\'] option[selected*=\'selected\']')[0].attrib['value']
        except:
            try:
                regexp = "http:\/\/images.asos-media.com\/inv\/media\/[\d]*\/[\d]*\/[\d]*\/[\d]*\/[\d]*\/([\w]*)\/[\d\w]*.jpg"
                result = re.search(regexp, image)
                color = result.group(1)
            except:
                color = ""
        return color
    
    def _get_title(self, itree):
    	try:
    	    title = itree.cssselect('div[class*=\'title\'] h1')[0].text_content().strip()
    	except:
        	title = ""
    	return unicode(title).encode('ascii', 'xmlcharrefreplace')
    
    def _get_category(self, itree):    
        try:
            category = itree.cssselect('div[id*=\'ctl00_ContentMainPage_productInfoPanel\'] strong')[0].text_content().strip()
        except:
            category = ""
        return unicode(category).encode('ascii', 'xmlcharrefreplace')