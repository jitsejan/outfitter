#!/usr/bin/env python
""" outfitter/create_messages.py """
import sqlalchemy.exc
import orm
import olog
import datetime

def create_message(session, user, date, products):
    """ Create a message for the email """
    olog.log('Creating message for ' +str(user.name), 'info')
    message = """\r\n
                <table class="table">
                  <tr>
                    <th>Product</th>
                    <th>Change</th>
                    <th>Old price</th>
                    <th>New price</th>\r\n"""
    for p in products:
        product = p[0]
        prices = p[1]
        olog.log(' ' +str(product.title)+ " " +str(product.link), 'debug')
        if len(prices) > 1:
            if prices[1].price != "" and prices[0].price != "":
                try:
                    pnew = prices[0].price.split(' ', 1)[0]
                    pnew = float(pnew.replace(',', '.').strip())
                except:
                    pnew = 0

                try:
                    pold = prices[1].price.split(' ', 1)[0]
                    pold = float(pold.replace(',', '.').strip())
                except:
                    pold = 0

                msg_str = "Old price <b>"+str(prices[1].price)+"</b>, "
                msg_str += "new price <b>"+str(prices[0].price)+"</b>"
                if pnew > pold:
                    clr = "red"
                    change = "Increase"
                elif pnew < pold:
                    clr = "green"
                    change = "Decrease"
                else:
                    clr = "yellow"
                    change = "No change"
                message += """
                            <tr>
                              <td><a href="%(link)s">%(title)s</a></td>
                              <td color="%(color)s">%(change)s</td>
                              <td>%(pricenew)s</td>
                              <td>%(priceold)s</td>
                            </tr>\r\n
                              """ % {'link' : str(p[0].link), 
                                     'title' : str(p[0].title), 
                                     'color' : clr, 
                                     'change' : change,
                                     'priceold' : str(prices[0].price),
                                     'pricenew' : str(prices[1].price)}
                
                olog.log(msg_str, pType=None, color=clr)
            elif(prices[1].price == "" and prices[0].price != ""):
                olog.log('Updated price for '+str(prices[0]), color="purple")
                message += """
                    <tr>
                        <td><a href="%(link)s">%(title)s</a></td>
                        <td color="blue">Back available</td>
                        <td></td>
                        <td>%(priceold)s</td>
                    </tr>\r\n
                    """ % {'link' : str(p[0].link), 
                           'title' : str(p[0].title), 
                           'priceold' : str(prices[0].price)}
            elif(prices[1].price != "" and prices[0].price == ""):
                olog.log('N.A.. Old price is '+str(prices[1]), color="blue")
                message += """
                <tr>
                    <td><a href="%(link)s">%(title)s</a></td>
                    <td color="yellow">N.A.</td>
                    <td>'+%(pricenew)s+'</td>
                    <td>'+%(priceold)s+'</td>
                </tr>\r\n
                """ % {'link' : str(p[0].link), 
                       'title' : str(p[0].title), 
                       'priceold' : str(prices[0].price),
                       'pricenew' : str(prices[1].price)
                }
        elif len(prices) == 1:
            message += '<tr><td><a href="'+str(p[0].link)+'">'+str(p[0].title)+'</a></td><td>New</td><td></td><td>'+str(prices[0].price)+'</td></tr>'

    message += '</table>'
    return message

def get_changed_prices(session, user, date):
    ''' gets products with changed prices '''
    products = []

    olog.log('Checking for ' +str(user.name)+ 'on ' +str(date), 'info')
    for product in session.query(orm.Product)\
     .outerjoin(orm.UserProduct, orm.UserProduct.productid == orm.Product.id)\
     .outerjoin(orm.ProductPrice, orm.ProductPrice.productid == orm.Product.id)\
     .filter(orm.UserProduct.userid == user.id)\
     .filter(orm.ProductPrice.checkdate == date):
        olog.log('Found product <b>' +str(product.title)+'</b>', 'debug')
        last_price = session.query(orm.ProductPrice)\
            .filter(orm.ProductPrice.productid == product.id)\
            .filter(orm.ProductPrice.checkdate == date)\
            .order_by("checkdate desc").first()
        if last_price:
            prices = session.query(orm.ProductPrice)\
                .filter(orm.ProductPrice.productid == product.id)\
                .filter(orm.ProductPrice.checkdate <= date)\
                .order_by("checkdate desc").limit(2).all()
            products.append([product, prices])

    return products

if __name__ == "__main__":
    session = orm.loadSession()

    for x in range(0, 1):
        timeoffset = x
        now = datetime.datetime.now()
        offset = datetime.timedelta(days=timeoffset)
        date = (now - offset).strftime('%Y-%m-%d')
        db_users = session.query(orm.User).all()
        for user in db_users:
            products = get_changed_prices(session, user, date)
            if(len(products) > 0):
                msg = create_message(session, user, date, products);
                if msg != "":
                    notification = orm.Notification(user.id, msg, False, date)
                    print notification
                    session.add(notification)
                    try:
                        session.commit()
                    except sqlalchemy.exc.IntegrityError as ex:
                        print ex
                        session.rollback()
