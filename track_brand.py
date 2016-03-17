################################################################################
# Application:      Outfitter
# File:             track_brand.py
# Goal:             
# Input:            
# Output:           
# Example:          
#
# History:          2016-02-09 - JJ     Creation of the file
#
################################################################################
import datetime
import re
import time
import urllib
import json

import orm

jsonString = """{
      "content" : [ {
        "key" : "TE4",
        "name" : "Ted Baker",
        "logoUrl" : "https://i2.ztat.net/brand/te4tedbakerlogo.jpg",
        "logoLargeUrl" : "https://i2.ztat.net/brandxl/te4tedbakerlogo.jpg",
        "shopUrl" : "https://www.zalando.nl/ted-baker"
      } ],
      "totalElements" : 1,
      "totalPages" : 1,
      "page" : 1,
      "size" : 1
    }
    """

jsonData = json.loads(jsonString)
print jsonData['content'][0]['key']

def parse_brand(json_str):
    data = json.loads(json_str)
    new_brand = orm.Brand()
    new_brand.name = data['content'][0]['name']
    

l = [1,2,3]
t = (1, 2, 3)
print l, t