#!/usr/bin/env python
from collections import defaultdict

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker
import sqlalchemy.exc
from productfactory import ProductFactory
import datetime
import orm
    
def get_changed_prices(session, user):
    ''' gets products with changed prices
    TODO: move to new module 'business_logic'?
    '''
    products = []
    for old_product in session.query(orm.Product).outerjoin(orm.UserProduct, orm.UserProduct.productid == orm.Product.id).filter(orm.UserProduct.userid == user.id):
      current_product = ProductFactory.create_product(old_product.link)
      if current_product.price.strip() is '':
          products.append([old_product, 'Not available'])
      elif current_product.price != old_product.price: #TODO: save new price to DB!
          products.append([old_product, current_product])
    return products

def get_images_for_product(session, productid):
    images = []
    for image in session.query(orm.ProductImage).\
                    filter(orm.ProductImage.productid == productid):
        images.append(image)
    return images
    
def get_prices_for_product(session, productid):
    prices = []
    for price in session.query(orm.ProductPrice).\
                    filter(orm.ProductPrice.productid == productid):
        prices.append(price)
    return prices

def get_users_for_product(session, productid):
    users = []
    for user in session.query(orm.UserProduct).\
                    filter(orm.UserProduct.productid == productid):
        users.append(user)
    return users

def get_outfits_for_product(session, productid):
    outfits = []
    for outfit in session.query(orm.OutfitProduct).\
                    filter(orm.OutfitProduct.productid == productid):
        outfits.append(outfit)
    return outfits

def remove_productimage(session, productimage):
    print 'Remove', productimage
    session.query(orm.ProductImage).\
        filter(orm.ProductImage.productid == productimage.productid).\
        filter(orm.ProductImage.imageurl == productimage.imageurl).\
        delete(synchronize_session='evaluate')
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError as ex:
        print ex
        session.rollback()

def remove_userproduct(session, userproduct):
    print 'Remove', userproduct
    session.query(orm.UserProduct).\
        filter(orm.UserProduct.productid == userproduct.productid).\
        filter(orm.UserProduct.userid == userproduct.userid).\
        delete(synchronize_session='evaluate')
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError as ex:
        print ex
        session.rollback()

def remove_productprice(session, productprice):
    print 'Remove', productprice
    session.query(orm.ProductPrice).\
        filter(orm.ProductPrice.productid == productprice.productid).\
        delete(synchronize_session='evaluate')
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError as ex:
        print ex
        session.rollback()

def remove_product(session, productid):
    print 'Remove', productid
    session.query(orm.Product).\
        filter(orm.Product.id == productid).\
        delete(synchronize_session='evaluate')
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError as ex:
        print ex
        session.rollback()

def update_outfitproduct(session, outfitproduct, newproductid):
    # Try to update the userproduct to the original product id
    print 'Update', outfitproduct, 'with productid', newproductid
    session.query(orm.OutfitProduct).\
        filter(orm.OutfitProduct.outfitid == outfitproduct.outfitid).\
        filter(orm.OutfitProduct.productid == outfitproduct.productid).\
        update({"productid": newproductid}, synchronize_session='evaluate')
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError as ex:
        print ex
        session.rollback()
        print 'Duplicate entry, already an entry for this outfitproduct. Remove the duplicate'
        # remove_outfitproduct(session, outfitproduct)
    
def update_userproduct(session, userproduct, newproductid):
    # Try to update the userproduct to the original product id
    print 'Update', userproduct, 'with productid', newproductid
    session.query(orm.UserProduct).\
        filter(orm.UserProduct.userid == userproduct.userid).\
        filter(orm.UserProduct.productid == userproduct.productid).\
        update({"productid": newproductid}, synchronize_session='evaluate')
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError as ex:
        print ex
        session.rollback()
        print 'Duplicate entry, already an entry for this userproduct. Remove the duplicate'
        remove_userproduct(session, userproduct)


################################################################################
# Function:         check_dead_products
# Input:            database session
# Output:           
# Goal:             Find dead products in the database and clean up
#                   if no user uses the product
# Targets:          
#
def check_dead_products(session):
    return True

################################################################################
# Function:         check_double_products
# Input:            database session
# Output:           
# Goal:             Find double products in the database and clean up
# Targets:          - Find double products in the products table
#                   - Find references in productimages table
#                   - Find references in productprices table
#                   - Find references in userproducts table
#
def check_double_products(session):
    print '\033[2;93m> Checking for double products.\033[0m'
    # Get all products from the database
    #
    # SQL: SELECT * FROM products
    db_products = session.query(orm.Product).all()
    # List of urls with the corresponding id(s)
    products = defaultdict(list)
    # Add the products to the list
    for product in db_products:
        products[product.link].append(product.id)
    # Loop through the products and verify if there are duplicates
    no_duplicates = 0
    for url, productids in products.iteritems():
        # Number of indices for the product
        len_indices = len(productids)
        # Check if there is more than 1 index
        if len_indices > 1:
            no_duplicates += 1
            print '\033[1;94m>> Found duplicate', url, '\033[0m'
            print '\033[1;95m>>> Product IDs',productids, '\033[0m'
            # Only change tables for the duplicates
            productid_org = productids.pop(0)
            for productid in productids:
                
                # References to duplicate product
                refs = 0
                print '\033[1;95m>>> Product ID', productid, '\033[0m'
            
                for productimage in get_images_for_product(session, productid):
                    refs += 1
                    remove_productimage(session, productimage)
                
                for productprice in get_prices_for_product(session, productid):
                    refs += 1
                    remove_productprice(session, productprice)
                
                for userproduct in get_users_for_product(session, productid):
                    refs += 1
                    update_userproduct(session, userproduct, productid_org)
                    
                for outfitproduct in get_outfits_for_product(session, productid):
                    refs += 1
                    update_outfitproduct(session, outfitproduct, productid_org)
            
                if refs > 0:
                    print '\033[2;91m<< Warning: References to the duplicate should be fixed\033[0m'
                else:
                    print 'Duplicate product has no references and can be removed'
                    remove_product(session, productid)
    print '\033[2;94m<< ', no_duplicates, 'duplicate(s) found.\033[0m'
    print '\033[2;93m< Done checking for double products.\033[0m'
    
    
def addproductimages(session):
    db_products = session.query(orm.Product).all()
    for product in db_products:
        print product.url
        current_product = ProductFactory.create_product(product.url)
        today = datetime.date.today()
        if current_product is not None:
            
            productprice = orm.ProductPrice(product.id, current_product.price, today)
            session.add(productprice)
            try:
                session.commit()
            except sqlalchemy.exc.IntegrityError as ex:
                print ex
                session.rollback()


            for image in current_product.images:
                productimage = orm.ProductImage(product.id, image)
                session.add(productimage)
                try:
                    session.commit()
                except sqlalchemy.exc.IntegrityError as ex:
                    print ex
                    session.rollback()

# def adduserproducts(session):
#     db_products = session.query(Product).all()
#     for product in db_products:
#         userproduct = UserProduct(product.userid, product.id)
#         session.add(userproduct)
#         try:
#             session.commit()
#         except sqlalchemy.exc.IntegrityError as ex:
#             print ex
#             session.rollback()
        
if __name__ == "__main__":
    session = orm.loadSession()
    check_double_products(session)
    
    #addproductimages(session)
    # adduserproducts(session)