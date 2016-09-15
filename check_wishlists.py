#!/usr/bin/env python
import sqlalchemy.exc

from productfactory import ProductFactory
import orm
import shortuuid
import datetime

def _insert_wishlist_uuid(session, wishlist):
    unique_id = str(shortuuid.uuid(str(wishlist.id) + wishlist.description))
    session.query(orm.Wishlist).\
        filter(orm.Wishlist.id == wishlist.id).\
        update({"uuid": unique_id}, synchronize_session='evaluate')
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError as ex:
        print ex
        session.rollback()

def _verify_uuids(session, wishlists):
    for wishlist in wishlists:
        if wishlist.uuid == '':
            _insert_wishlist_uuid(session, wishlist)
       
def _get_all_wishlists(session):
    ''' Gets all wishlists from database '''
    wishlists = []
    for wishlist in session.query(orm.Wishlist):
       wishlists.append(wishlist)

    return wishlists
    
if __name__ == "__main__":
    session = orm.loadSession()
    wishlists = _get_all_wishlists(session)
    _verify_uuids(session, wishlists)