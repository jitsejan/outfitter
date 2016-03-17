################################################################################
# Application:      Outfitter
# File:             topshop.py
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
import re
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

################################################################################
# Functions
################################################################################

################################################################################
# Classes
################################################################################

class TopshopTracker(Tracker):

    def __init__(self, *args, **kwargs):
        super(TopshopTracker,self).__init__('Topshop', *args, **kwargs)

    #############################################################################
    # Function:         _get_brands
    # Input:            
    # Output:           
    # Goal:             
    # Targets:          <div class="block_search_filter categoryBlock" id="category_0_998556" filter_id="1">
    #					    <div class="cf"><span class="filter_label">Category</span></div>
	#    		            <div class="cf">
    # 						<ul>
    #   						<li class="category_2823526" id="f_2823526" title="2823526">
    #                               <a href="http://eu.topman.com/en/tmeu/category/brands-617803/view-all-brands-1700863/amplified-5051590?N=10303+38063&Ndr=100000&Nr=OR%28product.emailBackInStock%3AY%2CNOT%28product.inventory%3A0%29%29&Nrpp=20&siteId=%2F13061"
    # 											removeaction=""
    # 											displayname = "TopMan_eu_category"
    # 											dim="?N=10303+38063&Ndr=100000&Nr=OR%28product.emailBackInStock%3AY%2CNOT%28product.inventory%3A0%29%29&Nrpp=20&siteId=%2F13061" title="Amplified">Amplified<span
    # 											class="item_count">(5)</span></a>
    #                   		</li>
    def _get_brands(self, session, insert):
        brands = []
        
        # Male
        # maleBrandsUrl = "http://eu.topman.com/en/tmeu/category/brands-617803/view-all-brands-1700863"
        
        # gender = "male"
        # olog.log("TopshopTracker._get_brands > Calling <b>"+maleBrandsUrl+"</b>", 'info')
        # hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729); nl-NL'}
        # req = urllib2.Request(maleBrandsUrl.replace(' ', '%20'), headers=hdr)
        # data = urllib2.urlopen(req).read()
        # tree = lxml.html.fromstring(data)

        # brand_data = tree.cssselect('div[class*=\"categoryBlock\"] ul li a')
        # for b in brand_data:
        #     brand = {'key' : None, 'name' : None, 'logoUrl' : None, 'logoLargeUrl' : None}
        #     brand['shopUrl'] = b.attrib['href']
        #     brand['name'] = unicode(b.attrib['title']).encode('ascii', 'xmlcharrefreplace')
        #     try:
        #         req = urllib2.Request(brand['shopUrl'], headers=hdr)
        #         adata = urllib2.urlopen(req).read()
        #         atree = lxml.html.fromstring(adata)
        #         brand['shopUrl'] = atree.cssselect('li[class*=\"show_all\"] a')[0].attrib['href']
        #     except:
        #         pass
            
        #     uuid = str(shortuuid.uuid(brand['name']))
        #     br = orm.Brand(brand['name'], brand['logoUrl'], brand['logoLargeUrl'], uuid)
        #     olog.log("TopshopTracker._get_brands << Found brand <b>"+str(br)+"</b>", 'debug')
            
        #     if insert is True:
        #         brand_in_db = session.query(orm.Brand).filter_by(name=unicode(br.name)).first()
        #         if brand_in_db is None:
        #             session.add(br)
        #             session.flush()
        #             brandid = br.id
        #             olog.log("TopshopTracker._get_brands >>> Inserted brand <b>"+br.name+"</b> with id <b>" + str(brandid) + "</b>", "warning")
        #         else:
        #             brandid = brand_in_db.id
        #             olog.log("Brand <b>"+brand_in_db.name+"</b> already in database with id <b>" + str(brandid) + "</b>", "debug")
                
        #         storebrand_in_db = session.query(orm.StoreBrand).filter_by(storeid=unicode(self.storeid)).filter_by(brandid=brandid).first()
        #         if storebrand_in_db is None:
        #             storebrand = {'key': None, 'storeid' : None, 'brandid' : None, 'gender': None, 'url' : None}
        #             sb = orm.StoreBrand(brand['key'], self.storeid, brandid, gender, brand['shopUrl'])
        #             olog.log("TopshopTracker._get_brands >>> Inserted <b>"+str(sb)+"</b>", "warning")
        #             session.add(sb)
        #             session.flush()


        #     brands.append(br)
      
        # Female
        femaleBrandsUrl = "http://eu.topshop.com/en/tseu/category/brands-a-to-z-4070022/home?TS=1422011935571"
        
        gender = "female"
        olog.log("TopshopTracker._get_brands > Calling <b>"+femaleBrandsUrl+"</b>", 'info')
         
        display = Display(visible=0, size=(800, 600))
        display.start()
        browser = webdriver.Firefox()
        browser.get(femaleBrandsUrl)
        data = browser.page_source
        browser.quit()
        display.stop()
        
        tree = lxml.html.fromstring(data)

        brand_data = tree.cssselect('div[class*=\"a-to-z\"] div[id*=\"jsonList\"] div[class*=\"columns\"] div div[class*=\"items\"] a')
        
        for b in brand_data:
            brand = {'key' : None, 'name' : None, 'logoUrl' : None, 'logoLargeUrl' : None}
            brand['shopUrl'] = b.attrib['href']
            brand['name'] = unicode(b.attrib['title'].title()).encode('ascii', 'xmlcharrefreplace')
            uuid = str(shortuuid.uuid(brand['name']))
            br = orm.Brand(brand['name'], brand['logoUrl'], brand['logoLargeUrl'], uuid)
            olog.log("TopshopTracker._get_brands << Found brand <b>"+str(br)+"</b>", 'debug')
            
            if insert is True:
                brand_in_db = session.query(orm.Brand).filter_by(name=unicode(br.name)).first()
                if brand_in_db is None:
                    session.add(br)
                    session.flush()
                    brandid = br.id
                    olog.log("TopshopTracker._get_brands >>> Inserted brand <b>"+br.name+"</b> with id <b>" + str(brandid) + "</b>", "warning")
                else:
                    brandid = brand_in_db.id
                    olog.log("Brand <b>"+brand_in_db.name+"</b> already in database with id <b>" + str(brandid) + "</b>", "debug")
                
                storebrand_in_db = session.query(orm.StoreBrand).filter_by(storeid=unicode(self.storeid)).filter_by(brandid=brandid).first()
                if storebrand_in_db is None:
                    storebrand = {'key': None, 'storeid' : None, 'brandid' : None, 'gender': None, 'url' : None}
                    sb = orm.StoreBrand(brand['key'], self.storeid, brandid, gender, brand['shopUrl'])
                    olog.log("TopshopTracker._get_brands >>> Inserted <b>"+str(sb)+"</b>", "warning")
                    session.add(sb)
                    session.flush()


            brands.append(br)
      
        session.commit()

        return brands
