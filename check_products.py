#!/usr/bin/env python
import sqlalchemy.exc
import olog
from productfactory import ProductFactory
import orm
import shortuuid
import datetime

def insert_product_uuid(session, url, productid):
    unique_id = str(shortuuid.uuid(url))
    session.query(orm.Product).\
        filter(orm.Product.id == productid).\
        update({"uuid": unique_id}, synchronize_session='evaluate')
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError as ex:
        print ex
        session.rollback()
        print 'Duplicate entry, already an entry for this outfitproduct. Remove the duplicate'
        # remove_outfitproduct(session, outfitproduct)

def update_product_category(session, product, productid):
    # Try to update the product to the original product id
    print 'Update', product, 'with productid', productid
    session.query(orm.Product).\
        filter(orm.Product.id == productid).\
        update({"category": product.category}, synchronize_session='evaluate')
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError as ex:
        print ex
        session.rollback()

def update_product(session, product, productid):
    # Try to update the product to the original product id
    print 'Update', product, 'with productid', productid
    session.query(orm.Product).\
        filter(orm.Product.id == productid).\
        update({"category": product.category}, synchronize_session='evaluate')
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError as ex:
        print ex
        session.rollback()

def update_product_brand(session, product, productid):
    # Try to update the product to the original product id
    print 'Update', product, 'with productid', productid
    session.query(orm.Product).\
        filter(orm.Product.id == productid).\
        update({"brand": product.brand}, synchronize_session='evaluate')
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError as ex:
        print ex
        session.rollback()

def get_changed_prices(session):
    ''' gets products with changed prices
    '''
    products = []
    today = datetime.date.today()
    print 'Today is', today
    for old_product in session.query(orm.Product):
        for last_price in session.query(orm.ProductPrice).filter(orm.ProductPrice.productid == old_product.id).order_by("checkdate desc").limit(1):
            lastprice = last_price.price
            if lastprice == None:
                lastprice = 0

        if(old_product.id != 0):
            current_product = ProductFactory.create_product(old_product.link)
            print 'Last price',lastprice, old_product.id
            print 'Current price', current_product.price
#             update_product_category(session, current_product, old_product.id)
#            update_product_brand(session, current_product, old_product.id)
#            insert_product_uuid(session, old_product.link, old_product.id)
            if current_product.price is None or current_product.price.strip() is '' or 'EUR' in current_product.price:
                products.append([old_product, 'Not available', lastprice])
                productprice = orm.ProductPrice(old_product.id, "", "", today)
                print productprice
                # Add new price to the productprice table
                session.add(productprice)
                try:
                    session.commit()
                except sqlalchemy.exc.IntegrityError as ex:
                    print ex
                    session.rollback()
            elif float(current_product.price) != float(lastprice):
            # Price has changed
            # Add to products array
                print 'Price has changed for', current_product.title,
                print 'Before', lastprice, 'Now', current_product.price
                products.append([old_product, current_product, lastprice])
                # Create product price object
                parray = current_product.price.split(" ")
                if len(parray) > 1:
                    currency = current_product.currency
                else:
                    currency = 'EUR'
                productprice = orm.ProductPrice(old_product.id, current_product.price, currency, today)
                print productprice
                # Add new price to the productprice table
                session.add(productprice)
                try:
                    session.commit()
                except sqlalchemy.exc.IntegrityError as ex:
                    print ex
                    session.rollback()
            else:
            	print 'No price change for', current_product.title
            
    return products

def add_storeids(session):
    ''' gets products '''
    # for old_product in session.query(orm.Product):
    #     for bla in session.query(orm.Store).filter(orm.Store.name == old_product.store).limit(1):
    #         old_product.storeid = bla.id
    #         update_product(session, old_product, old_product.id)

if __name__ == "__main__":
    session = orm.loadSession()
    db_users = session.query(orm.User).all()
    # add_storeids(session)
    products = get_changed_prices(session)
