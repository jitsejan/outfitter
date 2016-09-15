#!/usr/bin/env python
import sqlalchemy.exc

from productfactory import ProductFactory
import orm
import shortuuid
import datetime

def _insert_outfit_uuid(session, outfit):
    unique_id = str(shortuuid.uuid(str(outfit.id) + outfit.description))
    session.query(orm.Outfit).\
        filter(orm.Outfit.id == outfit.id).\
        update({"uuid": unique_id}, synchronize_session='evaluate')
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError as ex:
        print ex
        session.rollback()

def _verify_uuids(session, outfits):
    for outfit in outfits:
        if outfit.uuid == '':
            _insert_outfit_uuid(session, outfit)
       
def _get_all_outfits(session):
    ''' Gets all outfits from database '''
    outfits = []
    for outfit in session.query(orm.Outfit):
       outfits.append(outfit)

    return outfits
    
if __name__ == "__main__":
    session = orm.loadSession()
    outfits = _get_all_outfits(session)
    _verify_uuids(session, outfits)