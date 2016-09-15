#!/usr/bin/env python

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def _convert_html_to_txt(html):
    txt = ""
    txt = html.replace('<br/>', '\r\n')
    
    return txt

def create_price_notification(user, products):
    html = "<h1>A small update from Outfitter</h1>"
    html += "Hello "+user.name+"! The following item(s) have been changed in price:<br/><br/>"
    html += "<table>"
    diff = 0
    for product in products:
        old_product = product[0]
        new_product = product[1]
        lastprice = product[2]
        if diff is 0:
            html += '<tr><th>Store</th><th>Name</th><th>Old price</th><th>New price</th></tr>'
        diff +=1
        if new_product == 'Not available':
            html += '<tr><td>'+old_product.store+'</td><td><a href="'+old_product.url+'">'+ old_product.title +'</a></td><td>' + lastprice +'</td><td>Not available</td></tr>'
        else:
            html += '<tr><td>'+old_product.store+'</td><td><a href="'+old_product.url+'">'+ old_product.title +'</a></td><td>' + lastprice +'</td><td>'+ new_product.price+'</td></tr>'
    html += "</table>"
    html += "<br/>See you soon @ <a href='http://outfitter.jitsejan.nl'>Outfitter</a>!"

    txt = _convert_html_to_txt(html)
    return txt, html
    
def send_mail(subject, receiver, htmlcontent, textcontent):
    sender = "outfitter-mail@jitsejan.com"
    
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(textcontent, 'plain')
    part2 = MIMEText(htmlcontent, 'html')
    
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    
    # Send the message via local SMTP server.
    s = smtplib.SMTP('localhost')
    s.set_debuglevel(1)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(sender, receiver, msg.as_string())
    print s
    print 'Mail sent to', receiver
    s.quit()
