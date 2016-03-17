# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

# Create a text/plain message
msg = MIMEText("Testbericht")
me = "server@jitsejan.nl"
you = "mail@jitsejan.com"
msg['Subject'] = 'The contents of the content'
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('localhost', 26)
s.sendmail(me, [you], msg.as_string())
s.quit()


sender = me
receivers = you

message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
   smtpObj = smtplib.SMTP('localhost', 26)
   smtpObj.sendmail(sender, receivers, message)         
   print "Successfully sent email"
except:
   print "Error: unable to send email"
   
   