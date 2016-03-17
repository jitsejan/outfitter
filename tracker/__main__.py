
################################################################################
# Application:      Outfitter
# File:             __main__.py
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
import sys
from tracker import Tracker
import orm
import olog
from outfitter.tracker import asos, zalando, sarenza, topshop, clarks, tedbaker, bijenkorf, netaporter
################################################################################
# Definitions
################################################################################
author =    "JJ"
appName =   "Outfitter"
verbosity = 0
################################################################################
# Functions
################################################################################

################################################################################
# main
################################################################################
if __name__ == "__main__": 
    session = orm.loadSession()
    if len(sys.argv) > 1:
        verbosity = sys.argv[2]
    

    ntracker = netaporter.NetaporterTracker()
    #ntracker._set_brands(session, insert=False)
    ntracker._brands = ntracker._get_brands(session)
    for storebrand in ntracker._brands:
        # print storebrand[1].name
        #if 'Dio' in storebrand[1].name:
        pass #items = ntracker._set_items_for_brand(storebrand[0], session, insert=True)

    btracker = bijenkorf.BijenkorfTracker()
    # btracker._set_brands(session, insert=True)
    # btracker._brands = btracker._get_brands(session)
    # for storebrand in btracker._brands:
    #     # if 'Armani' in storebrand[1].name:
    #     items = btracker._set_items_for_brand(storebrand[0], session, insert=True)

    
    ztracker = zalando.ZalandoTracker()
    # ztracker._set_brands(session, insert=False)
    ztracker._brands = ztracker._get_brands(session)
    for storebrand in ztracker._brands:
        ztracker._get_items_for_brand(storebrand[0], session, insert=True)

    tedtracker = tedbaker.TedBakerTracker()
    #tedtracker._set_brands(session, insert=False)
    tedtracker._brands = tedtracker._get_brands(session)
    for storebrand in tedtracker._brands:
        print storebrand
        # tedtracker._set_items_for_brand(storebrand[0], session, insert=True)
       
    # ctracker = clarks.ClarksTracker()
    # ctracker._set_brands(session, insert=True)
    # ctracker._brands = ctracker._get_brands(session)
    # for brand in ctracker._brands:
    #     pass#    ctracker._set_items_for_brand(brand, session, insert=True)
    
    
    # ztracker._get_item(aid
    
    # atracker = asos.AsosTracker()
    # atracker._brands = atracker._set_brands(session, insert=True)
    
    # stracker = sarenza.SarenzaTracker()
    # stracker._brands = stracker._set_brands(session, insert=True)
    # stracker._brands = stracker._get_brands(session)
    # for storebrand in stracker._brands:
    #     items = stracker._set_items_for_brand(storebrand[0], session, insert=True)
    
    
    
    # toptracker = topshop.TopshopTracker()
    # toptracker._brands = toptracker._get_brands(session, insert=True)
    
    # stores = session.query(orm.Store).all()
    # for store in stores:
    #     if store.id == 1:
    #         storebrands = session.query(orm.StoreBrand).join(orm.Brand, orm.StoreBrand.brandid == orm.Brand.id)\
    #                                          .filter(orm.StoreBrand.storeid == store.id).all()
    #         print store.name + " has " + str(len(storebrands)) + " brands"                              
    #         b = 0
    #         for brand in storebrands:
    #             if store.name == 'Asos':
    #                 pass #atracker._get_items_for_brand(brand, session, insert=True)
    #             if store.name == 'Zalando':
    #                 ztracker._get_items_for_brand(brand, session, insert=True)
    #                 b +=1
                
    #             if b == 10:
    #                 break
    #         break
