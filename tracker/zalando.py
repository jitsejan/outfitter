################################################################################
# Application:      Outfitter
# File:             zalando.py
# Goal:             
# Input:            
# Output:           
# Example:          
# Info:             https://api.zalando.com/
#
# History:          2016-02-10 - JJ     Creation of the file
#
################################################################################

################################################################################
# Imports
################################################################################
from tracker import Tracker
import orm
import olog
import json
import urllib, urllib2
import unidecode
import shortuuid
import time

################################################################################
# Definitions
################################################################################
author =    "JJ"
appName =   "Outfitter"

hdr = {'Accept-Language': 'nl-NL', 'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; nl-NL; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729); nl-NL'}

################################################################################
# Functions
################################################################################

################################################################################
# Classes
################################################################################

class ZalandoTracker(Tracker):

    def __init__(self, *args, **kwargs):
        super(ZalandoTracker,self).__init__('Zalando', *args, **kwargs)

    def _get_number_of_brands(self, session):
        storebrands = session.query(orm.StoreBrand).join(orm.Brand, orm.StoreBrand.brandid == orm.Brand.id)\
                                              .filter(orm.StoreBrand.storeid == self.storeid).all()
        return len(storebrands)
    
    #############################################################################
    # Function:         _set_brands
    # Input:            
    # Output:           
    # Goal:             
    # Targets:          
    # 
    def _set_brands(self, session, insert):
        global hdr
        brands = []
        
        maxPageSize = 200
        brandsUrl = "https://api.zalando.com/brands?pageSize="+str(maxPageSize)
        
        olog.log("ZalandoTracker._set_brands > Calling <b>"+brandsUrl+"</b>", 'info')
        
        
        req = urllib2.Request(brandsUrl, headers=hdr)
        brandsJson =  json.loads(urllib2.urlopen(req).read())
        
        totalElements = brandsJson['totalElements']
        
        pages = brandsJson['totalPages']
        insertedElements = 0
        for page in range(pages):
            brandUrl = brandsUrl+"&page="+str(page+1)
            
            olog.log("ZalandoTracker._set_brands >> Calling <b>"+brandUrl+"</b>,", 'debug')

            brandJson = json.loads(urllib.urlopen(brandUrl).read())
            bcounter = 0
            for b in brandJson['content']:
                brand = {'logoUrl' : None, 'logoLargeUrl' : None, 'shopUrl' : None}
                brand.update(b)
                brand['name'] = unicode(brand['name']).encode('ascii', 'xmlcharrefreplace')
                uuid = str(shortuuid.uuid(brand['name']))
                br = orm.Brand(brand['name'], brand['logoUrl'], brand['logoLargeUrl'], uuid)
                olog.log("ZalandoTracker._set_brands << Found <b>"+br.name+"</b>", 'debug')
                
                if insert is True:
                    brand_in_db = session.query(orm.Brand).filter_by(name=unicode(br.name)).first()
                    if brand_in_db is None:
                        session.add(br)
                        session.flush()
                        brandid = br.id
                        olog.log("ZalandoTracker._set_brand >>> Inserted brand <b>"+str(br)+"</b> with id <b>" + str(brandid) + "</b>", "warning")
                        insertedElements += 1
                    else:
                        brandid = brand_in_db.id
                        olog.log("ZalandoTracker._set_brand >>> Brand <b>"+brand_in_db.name+"</b> already in database with id <b>" + str(brandid) + "</b>", "debug")
                    
                    storebrand_in_db = session.query(orm.StoreBrand).filter_by(storeid=unicode(self.storeid)).filter_by(brandid=brandid).first()
                    if storebrand_in_db is None:
                        storebrand = {'key': None, 'storeid' : None, 'brandid' : None, 'gender' : None, 'url' : None}
                        sb = orm.StoreBrand(brand['key'], self.storeid, brandid, None, brand['shopUrl'])
                        olog.log("ZalandoTracker._set_brands >>> Inserted <b>"+str(sb)+"</b>", "warning")
                        session.add(sb)
                        session.flush()
                    bcounter += 1
                
                brands.append(br)
        session.commit()
        olog.log("ZalandoTracker._set_brands < Number of brands is <b>"+str(totalElements)+"</b>", 'info')
        olog.log("ZalandoTracker._set_brands < Inserted brands is <b>"+str(insertedElements)+"</b>", 'info')
        return brands
        
    def _get_items_for_brand(self, brand, session, insert):
        global hdr
        items = []
        maxPageSize = 200
        articlesURL = "https://api.zalando.com/articles?pageSize="+str(maxPageSize)+"&brand=" + str(brand.key)
        
        olog.log("ZalandoTracker._get_items_for_brand >>> Get articles <b>"+articlesURL+"</b>", 'debug')

        req = urllib2.Request(articlesURL, headers=hdr)
        try:
            articlesJson =  json.loads(urllib2.urlopen(req).read())
        
            date = time.strftime('%Y-%m-%d %H:%M:%S')
    
            pages = articlesJson['totalPages']
            totalElements = articlesJson['totalElements']
            olog.log("ZalandoTracker._get_items_for_brand <<< Number of items <b>"+str(totalElements)+"</b>", 'debug')
            if totalElements > 0:
                acounter = 1
                for page in range(pages):
                    articleURL = articlesURL+"&page="+str(page+1)+"&fields=id"
                    olog.log("ZalandoTracker._get_items_for_brand >>>> Get articles per page <b>"+str(articleURL)+"</b>", 'debug')
                    articleJson = json.loads(urllib.urlopen(articleURL).read())
                    for article in articleJson['content']:
                        if article is not None:
                            iid = article['id']
                            i = session.query(orm.Item).filter_by(itemid=iid).filter_by(storeid=self.storeid).first()
                            if i is None:
                                item = self._get_item(brand, iid)
                                if item is not False:
                                    i = orm.Item(item['storeid'], item['itemid'], item['brandid'], item['link'], item['color'], item['title'], item['category'], item['gender'], item['uuid'])
                                    olog.log("ZalandoTracker._get_items_for_brand <<<< "+str(acounter)+'/'+str(totalElements)+" Found item <b>"+str(i)+"</b>", "warning")                                    
                                    if insert is True:
                                        session.add(i)
                                        session.flush()
                                        itemid = i.id
                                        olog.log("ZalandoTracker._get_items_for_brand >>> Inserted item <b>"+str(i)+"</b> with id <b>" + str(itemid) + "</b>", "warning")
                                        for imageurl in item['images']:
                                            ii = session.query(orm.ItemImage).filter_by(itemid=itemid).filter_by(imageurl=imageurl).first()
                                            if ii is None:
                                                ii = orm.ItemImage(itemid, imageurl)
                                                olog.log("ZalandoTracker._get_items_for_brand <<<< Inserted image <b>"+str(ii)+"</b>", "warning")
                                                session.add(ii)
                                            else:
                                                olog.log("ZalandoTracker._get_items_for_brand <<<< Image <b>"+str(ii)+"</b> akready in database", "info")
                                        ip = orm.ItemPrice(itemid, item['price'], item['currency'], date)
                                        olog.log("ZalandoTracker._get_items_for_brand <<<< Inserted price <b>"+str(ip)+"</b>", "warning")
                                        session.add(ip)
                                    items.append(i)
                                #endif item is not False
                            else:
                                itemid = i.id
                                olog.log("ZalandoTracker._get_items_for_brand <<<< "+str(acounter)+" <b>"+i.title+"</b> already in database with id <b>" + str(itemid) + "</b>", "info")
                                items.append(i)
                            acounter += 1
                            #endif i is None
                        #endif it is not None
                    #endfor it in articleJson['content']
                #endfor for page in range(pages)
                if insert is True:
                    session.commit()
            #endif for totalElements >)
        except:
            pass # Brand URL does not work
        
        return items
    
    def _get_item(self, brand, itemid):
        global hdr
        itemURL = "https://api.zalando.com/articles?articleID="+itemid
        
        # olog.log("ZalandoTracker._get_item >>>> Calling <b>"+itemURL+"</b>", 'debug')
        req = urllib2.Request(itemURL, headers=hdr)
        itemJson = json.loads(urllib2.urlopen(req).read())
        
        try:
            item = {}
            item['storeid'] = self.storeid
            item['brandid'] = brand.brandid
            item['itemid'] = itemJson['content'][0]['id']
            item['title'] = unicode(itemJson['content'][0]['name']).encode('ascii', 'xmlcharrefreplace')
            item['link'] = itemJson['content'][0]['shopUrl']
            item['color'] = itemJson['content'][0]['color']
            item['category'] = itemJson['content'][0]['categoryKeys'][4]
            item['brand'] = itemJson['content'][0]['brand']['name']
            item['price'] = itemJson['content'][0]['units'][0]['price']['value']
            item['currency'] = itemJson['content'][0]['units'][0]['price']['currency']
            item['gender'] =  ', '.join(itemJson['content'][0]['genders'])
            item['uuid'] = str(unicode(shortuuid.uuid(item['link'].encode('ascii', 'xmlcharrefreplace'))))
            item['images'] = []
            for image in itemJson['content'][0]['media']['images']:
                item['images'].append(image['largeUrl'])
            return item
        except:
            olog.log("ZalandoTracker._get_item >>>> Error for <b>"+itemURL+"</b>", 'error')
            return False
        