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
from outfitter.tracker import zalando
from outfitter.tracker import asos, bijenkorf

coloredlogs.install(level='DEBUG')

logger = logging.getLogger('outfitter')
logger.setLevel(logging.DEBUG)

################################################################################
# Definitions
################################################################################

def get_all_items_in_db(session, limit):
    logger.info('Limit is '+str(limit))
    print 'Item.delete_all\r\n'
    items = session.query(orm.Item)\
                   .limit(limit)\
                   .all()
    for item in items:
        if item._to_json() is not None:
            print item._to_json()


def get_tracker(session, store):
    """ Returns the tracker for a given store """
    if store == 'zalando':
        tracker = zalando.ZalandoTracker(session)
    elif store == 'bijenkorf':
        tracker = bijenkorf.BijenkorfTracker(session)
    elif store == 'asos':
        tracker = asos.AsosTracker(session)
    else:
        logger.error('< Unknown store. Exiting')
        sys.exit()
    return tracker

################################################################################
# Functions
################################################################################

def main():
    """ Main function """
    stores = ['zalando', 'bijenkorf', 'asos']
    actions = ['brands', 'new', 'all', 'test']
    parser = ArgumentParser()
    parser.add_argument("-s", "--store", dest="store", default=None,
    choices=stores, help="Store")
    parser.add_argument("-a", "--action", dest="action", default=None,
    choices=actions, help="Action")
    parser.add_argument("-l", "--link", dest="link", default=None, help="Link")
    args = parser.parse_args()
    session = orm.loadSession()
    logger.debug('> Loading session..')
    if args.link is not None:
        if 'zalando.' in args.link or 'zln.do' in args.link:
            tracker = zalando.ZalandoTracker(session)
        elif 'bijenkorf' in args.link:
            tracker = bijenkorf.BijenkorfTracker(session)
        elif 'asos.' in args.link:
            tracker = asos.AsosTracker(session)
        else:
            logger.error('Tracker not available')
            sys.exit()
        itemid = tracker._get_item_id(args.link)
        if itemid:
            item = tracker._get_item(itemid)
            if item is not None:
                logger.info("< Found " +str(item)+ " in DB")
            else:
                logger.warning("< No item found! Need to parse")
                item = tracker._get_item_data(args.link)
                if item:
                    logger.info("< Found " +str(item)+ "")
                else:
                    logger.error("< No item found")
        else:
            logger.error('< Item ID not found')
    elif args.store is not None and args.action is not None:
        tracker = get_tracker(session, args.store)
        if args.action == 'brands':
            tracker._set_brands(session, insert=True)
        elif args.action == 'new':
            tracker._get_new_items(session)
        elif args.action == 'all':
            tracker._get_all_items(session)
        else:
            logger.error('< Unknown action. Exiting')
            sys.exit()
    else:
        limit = 5
        tracker = zalando.ZalandoTracker(session)
        items = tracker.get_new_items()
        print items
        #get_all_items_in_db(session, limit)
        #logger.error('< Nothing to do. Use -h to show the help')
    session.close()

################################################################################
# main
################################################################################
if __name__ == "__main__":
    main()
