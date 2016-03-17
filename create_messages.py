#!/usr/bin/env python
import sqlalchemy.exc
import orm
import olog
import datetime

def create_message(session, user, date, products):
    olog.log('Creating message for ' +str(user.name), 'info')
    message = '\r\n<table class="table"><tr><th>Product</th><th>Change</th><th>Old price</th><th>New price</th>\r\n'
    for p in products:
        product = p[0]
        prices = p[1]
        olog.log(' ' +str(product.title)+ " " +str(product.link), 'debug')
        if len(prices) > 1:
            if(prices[1].price != "" and prices[0].price != ""):
                try:
                    pnew = float(prices[0].price.split(' ', 1 )[0].replace(',', '.').strip())
                except:
                    pnew = 0

                try:
                    pold = float(prices[1].price.split(' ', 1 )[0].replace(',', '.').strip())
                except:
                    pold = 0

                if pnew > pold:
                    olog.log('Old price <b>'+str(prices[1].price)+"</b>, new price <b>"+str(prices[0].price)+"</b>", pType=None, color="red")
                    message += '<tr><td><a href="'+str(p[0].link)+'">'+str(p[0].title)+'</a></td><td color="red">Increase</td><td>'+str(prices[1].price)+'</td><td>'+str(prices[0].price)+'</td></tr>\r\n'
                elif pnew < pold:
                    olog.log('Old price <b>'+str(prices[1].price)+"</b>, new price <b>"+str(prices[0].price)+"</b>", pType=None, color="green")
                    message += '<tr><td><a href="'+str(p[0].link)+'">'+str(p[0].title)+'</a></td><td color="green">Decrease</td><td>'+str(prices[1].price)+'</td><td>'+str(prices[0].price)+'</td></tr>\r\n'
                else:
                    olog.log('Old price <b>'+str(prices[1].price)+"</b>, new price <b>"+str(prices[0].price)+"</b>", pType=None, color="yellow")
                    # message += '<td><a href="'+str(p[0].link)+'">'+str(p[0].title)+'</a></td><td color="orange">None</td><td>'+str(prices[1].price)+'</td><td>'+str(prices[0].price)+'</td></tr>\r\n'
            elif(prices[1].price == "" and prices[0].price != ""):
                olog.log('Updated price for '+str(prices[0]), pType=None, color="purple")
                message += '<tr><td><a href="'+str(p[0].link)+'">'+str(p[0].title)+'</a></td><td color="blue">Back available</td><td></td><td>'+str(prices[0].price)+'</td></tr>\r\n'
            elif(prices[1].price != "" and prices[0].price == ""):
                olog.log('Not available anymore. Previous price is '+str(prices[1]), pType=None, color="blue")
                message += '<tr><td><a href="'+str(p[0].link)+'">'+str(p[0].title)+'</a></td><td color="yellow">N.A.</td><td>'+str(prices[1].price)+'</td><td>'+str(prices[0].price)+'</td></tr>\r\n'
        elif(len(prices) == 1):
            message += '<tr><td><a href="'+str(p[0].link)+'">'+str(p[0].title)+'</a></td><td>New</td><td></td><td>'+str(prices[0].price)+'</td></tr>'



    message += '</table>'
    return message

def get_changed_prices(session, user, date):
    ''' gets products with changed prices
    '''
    products = []

    olog.log('Checking for ' +str(user.name)+ 'on ' +str(date), 'info')
    for product in session.query(orm.Product).outerjoin(orm.UserProduct, orm.UserProduct.productid == orm.Product.id)\
                                             .outerjoin(orm.ProductPrice, orm.ProductPrice.productid == orm.Product.id)\
                                         .filter(orm.UserProduct.userid == user.id)\
                                         .filter(orm.ProductPrice.checkdate == date):
        olog.log('Found product <b>' +str(product.title)+'</b>', 'debug')
        last_price = session.query(orm.ProductPrice).filter(orm.ProductPrice.productid == product.id).filter(orm.ProductPrice.checkdate == date).order_by("checkdate desc").first()
        if last_price:
            prices = session.query(orm.ProductPrice).filter(orm.ProductPrice.productid == product.id).filter(orm.ProductPrice.checkdate <= date).order_by("checkdate desc").limit(2).all()
            products.append([product, prices])

    return products

if __name__ == "__main__":
    session = orm.loadSession()

    for x in range(0, 1):
        timeoffset = x

        date = (datetime.datetime.now() - datetime.timedelta(days=timeoffset)).strftime('%Y-%m-%d')
        db_users = session.query(orm.User).all()
        for user in db_users:
            products = get_changed_prices(session, user, date)
            if(len(products) > 0):
                message = create_message(session, user, date, products);
                if message != "":
                    notification = orm.Notification(user.id, message, False, date)
                    print notification
                    session.add(notification)
                    try:
                        session.commit()
                    except sqlalchemy.exc.IntegrityError as ex:
                        print ex
                        session.rollback()
