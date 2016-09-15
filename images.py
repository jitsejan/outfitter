#!/usr/bin/env python
import sqlalchemy.exc
import orm
import urllib
import os

def update_productimage(session, imageurl, id):
    # Try to update the userproduct to the original product id
    print 'Add', imageurl, 'for id', id
    session.query(orm.ProductImage).\
        filter(orm.ProductImage.id == id).\
        update({"localurl": imageurl}, synchronize_session='evaluate')
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError as ex:
        print ex
        session.rollback()
        print 'Duplicate entry, already an entry for this productimage. Remove the duplicate'
        # remove_userproduct(session, userproduct)

def get_all_images(session):
    ''' Gets images
    '''
    products = []
    # session.query(orm.Product).outerjoin(orm.UserProduct, orm.UserProduct.productid == orm.Product.id).filter(orm.UserProduct.userid == user.id):
    for p in session.query(orm.ProductImage, orm.Product)\
    							    .outerjoin(orm.Product, orm.Product.id==orm.ProductImage.productid)\
									.order_by(orm.ProductImage.id):
		
        products.append([p[0].productid, p[0].imageurl, p[1].uuid, p[0].id])

    return products
    
if __name__ == "__main__":
    session = orm.loadSession()
    products = get_all_images(session)
    productids = []
    i = 0
    for product in products:
		if product[0] not in productids and ('ztat' in product[1] or 'tommy' in product[1] or 'topman' in product[1]):
			print 'adding', product[0]
			productids.append(product[0])
			if product[1].startswith('//'):
				product[1] = "http:"+product[1].split("?")[0]
			head, tail = os.path.split(product[1])
			print 'Retrieving image ' + product[1]
			saveFile = "/home/jitsejan/sites/scripts/" + product[2] + ".jpg"
			print 'Save', saveFile
			outputFile = "/home/jitsejan/sites/scripts/" + product[2] + ".png"
			print 'Output', outputFile
			try:
# 				urllib.urlretrieve(product[1], outputFile)
				getCmd = "wget -O " + saveFile + " " +product[1]
				os.system(getCmd)
				# cmd = 'convert '+ tail +' -fuzz 3% -fill none -draw "matte 0,0 replace" '+ tail.replace('.jpg', '_c.png')
				# print 'Convert call', cmd
				cmd = 'convert '+ saveFile +' -fuzz 3% -fill none -draw "matte 0,0 replace" '+ outputFile.replace('.', '_c.')
				print 'Convert call', cmd
				os.system(cmd)
# 				convert image1xxl.jpg -fuzz 10% -fill none -draw "matte 0,0 replace" image1xxl.PNG
# 				convert rose: -format '%[pixel:p{40,30}]' info:-
				# cmd2 = "mogrify -format png -median 2 -fuzz 1% -transparent white " + saveFile
				# print 'Mogrify call', cmd2
				# os.system(cmd2)
				update_productimage(session, outputFile.replace('.', '_c.'), product[3])
				print ' => OK '
			except:
				print ' => NOK '
			i += 1
# 		else:
# 			print 'ignoring', product[0]    	
			
		# if i == 1:
			# break