#!/usr/bin/env python
import sqlalchemy.exc

from productfactory import ProductFactory
import orm
import shortuuid
import datetime

def _update_product_price(session, productprice):
    # Try to update the product to the original product id
    print 'Update', productprice, 'with productid', productprice.productid
    session.query(orm.ProductPrice).\
        filter(orm.ProductPrice.id == productprice.productid).\
        update({"MyColNum": productprice.price}, synchronize_session='evaluate')
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError as ex:
        print ex
        session.rollback()
       
def _get_all_product_prices(session):
    ''' Gets all productprices from database '''
    productprices = []
    for productprice in session.query(orm.ProductPrice):
        if productprice.price is "":
            print '-> Empty'
        else:
            parray = productprice.price.split(" ")
            
            try:
                productprice.MyColNum = float(parray[0].replace(',', '.'))
            except:
                productprice.MyColNum = ""
            
            if len(parray) > 1:
                productprice.currency = parray[1]
        productprices.append(productprice)
        
    return productprices
    
if __name__ == "__main__":
    session = orm.loadSession()
    productprices = _get_all_product_prices(session)
    for p in productprices:
        pass
        # _update_product_price(session, p)