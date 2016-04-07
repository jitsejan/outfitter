
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


def netaporter_process():
    ntracker = netaporter.NetaporterTracker(session)
    #ntracker._set_brands(session, insert=False)
    for storebrand in ntracker._brands:
        # print storebrand[1].name
        #if 'Dio' in storebrand[1].name:
        pass #items = ntracker._set_items_for_brand(storebrand[0], session, insert=True)

def bijenkorf_process():
    btracker = bijenkorf.BijenkorfTracker(session)
    #btracker._set_brands(session, insert=True)
    for storebrand in btracker._brands:
        items = btracker._get_items_for_brand(storebrand[0], session, insert=True, thisweekonly=True)

def tedbaker_process():
    tedtracker = tedbaker.TedBakerTracker(session)
    #tedtracker._set_brands(session, insert=False)
    #tedtracker._get_brands(session)
    for storebrand in tedtracker._brands:
        pass #    print storebrand
        # tedtracker._set_items_for_brand(storebrand[0], session, insert=True)

def clark_process():
    ctracker = clarks.ClarksTracker(session)
    # ctracker._set_brands(session, insert=True)
    # ctracker._brands = ctracker._get_brands(session)
    # for brand in ctracker._brands:
    #     pass#    ctracker._set_items_for_brand(brand, session, insert=True)

def asos_process():
    atracker = asos.AsosTracker()
    # atracker._brands = atracker._set_brands(session, insert=True)

def sarenza_process():
    stracker = sarenza.SarenzaTracker(session)
    #stracker._brands = stracker._set_brands(session, insert=True)
    stracker._brands = stracker._get_brands(session)
    for storebrand in stracker._brands:
        pass#  items = stracker._set_items_for_brand(storebrand[0], session, insert=True)

def topshop_process():
    toptracker = topshop.TopshopTracker(session)
    # toptracker._brands = toptracker._get_brands(session, insert=True)

################################################################################
# main
################################################################################
if __name__ == "__main__": 
    session = orm.loadSession()
    if len(sys.argv) > 1:
        verbosity = sys.argv[2]
    
    ztracker = zalando.ZalandoTracker(session)
    ztracker._get_new_items(session)

    ztracker = zalando.ZalandoTracker(session)
    ztracker._get_new_items(session)



































































































































