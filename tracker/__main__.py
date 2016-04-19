""" tracker/__main__.py """
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
__author__ = "Jitse-Jan van Waterschoot"
__copyright__ = "Copyright 2015-2016"
__credits__ = ["JItse-Jan van Waterschoot"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jitse-Jan van Waterschoot"
__email__ = "mail@jitsejan.nl"
__status__ = "Production"

################################################################################
# Imports
################################################################################
import coloredlogs
import sys
from argparse import ArgumentParser
import logging
import orm
from outfitter.tracker import asos, zalando, sarenza, topshop, clarks
from outfitter.tracker import bijenkorf, netaporter, tedbaker

coloredlogs.install(level='DEBUG')

logger = logging.getLogger('outfitter')
logger.setLevel(logging.INFO)

################################################################################
# Definitions
################################################################################

################################################################################
# Functions
################################################################################

def netaporter_process():
    """ Starts a Net-A-Porter tracker """
    ntracker = netaporter.NetaporterTracker(session)
    #ntracker._set_brands(session, insert=False)
    # for storebr in ntracker._brands:
    #    items = ntracker._set_items_for_brand(storebr[0], session, insert=True)
    #     pass
    return ntracker

def tedbaker_process():
    """ Starts a Ted Baker tracker """
    tedtracker = tedbaker.TedBakerTracker(session)
    #tedtracker._set_brands(session, insert=False)
    #tedtracker._get_brands(session)
    # for storebrand in tedtracker._brands:
        # pass #    print storebrand
        # tedtracker._set_items_for_brand(storebrand[0], session, insert=True)
    return tedtracker

def clark_process():
    """ Starts a Clarks tracker """
    ctracker = clarks.ClarksTracker(session)
    # ctracker._set_brands(session, insert=True)
    # ctracker._brands = ctracker._get_brands(session)
    # for brand in ctracker._brands:
    #     pass#    ctracker._set_items_for_brand(brand, session, insert=True)
    return ctracker

def asos_process():
    """ Starts an Asos Tracker """
    atracker = asos.AsosTracker()
    # atracker._brands = atracker._set_brands(session, insert=True)
    return atracker

def sarenza_process():
    """ Starts a Sarenza tracker """
    stracker = sarenza.SarenzaTracker(session)
    #stracker._brands = stracker._set_brands(session, insert=True)
    # stracker._brands = stracker._get_brands(session)
    # for storeb in stracker._brands:
        #items = stracker._set_items_for_brand(storeb[0], session, insert=True)
        # pass
    return stracker

def topshop_process():
    """ Starts a Topshop tracker """
    toptracker = topshop.TopshopTracker(session)
    # toptracker._brands = toptracker._get_brands(session, insert=True)
    return toptracker


def main():
    """ Main function """
    stores = ['zalando', 'bijenkorf']
    actions = ['brands', 'new', 'test']
    parser = ArgumentParser()
    parser.add_argument("-s", "--store", dest="store", default=None,
    choices=stores, help="Store")
    parser.add_argument("-a", "--action", dest="action", default=None,
    choices=actions, help="Action")
    parser.add_argument("-l", "--link", dest="link", default=None,
    help="Link")
    args = parser.parse_args()
    
    session = orm.loadSession()
    logger = logging.getLogger('outfitter')
    logger.debug('Loading session..')
    
    if args.link is not None:
        if 'zalando.' or 'zln.do' in args.link:
            logger.debug('Initializing ZalandoTracker')
            ztracker = zalando.ZalandoTracker(session)
            itemid = ztracker._get_item_id(args.link)
            if itemid:
                item = ztracker._get_item(itemid)
                if item:
                    print item
            else:
                logger.error('Item ID not found')
        else:
            logger.error('Tracker not available')
            

    elif args.store is not None:
        if args.store == 'zalando':
            logger.debug('Initializing ZalandoTracker')
            tracker = zalando.ZalandoTracker(session)      
            if args.action is not None:
                if args.action == 'brands':
                    logger.debug('Setting brands for ZalandoTracker')
                    tracker._set_brands(session, insert=True)
                elif args.action == 'new':
                    logger.debug('Getting new items for ZalandoTracker')
                    tracker._get_new_items(session)
                else:
                    brand = tracker._get_storebrand('Walra')
                    zitems = zracker._get_items_for_brand(brand, session, insert=True, thisweekonly=False)

            else:
                logger.error("No action chosen!")
        elif args.store == 'bijenkorf':
            logger.debug('Initializing BijenkorfTracker')
            tracker = bijenkorf.BijenkorfTracker(session)      
            if args.action is not None:
                if args.action == 'brands':
                    logger.debug('Setting brands for BijenkorfTracker')
                    tracker._set_brands(session, insert=True)
                elif args.action == 'new':
                    logger.debug('Getting new items for BijenkorfTracker')
                    tracker._get_new_items(session)
                else:
                    pass
            else:
                logger.error("No action chosen!")
    
    
    btracker = bijenkorf.BijenkorfTracker(session)
    # btracker._get_new_items(session)

    

################################################################################
# main
################################################################################
if __name__ == "__main__":
    main()