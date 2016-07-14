# README #
This repository contains the first version of the Outfitter appplication. At this moment the project has been put on hold. I am working on a second version which can crawl the whole page and puts data in the MySQL database.

### What does Outfitter do? ###
Outfitter crawls information for a given link from any of the supported webstore. When it receives a link, it will automatically search for the corresponding data in the web store. It only takes care of the back-end of the database. Visualisation is done on a webpage currently created with Code Igniter. On this page you can insert a product link, Outfitter will return the product data and the product will be added to your items on the web page. Once a product is in the database, a script will check the price of the item every day and indicate the price change. 

### Supported webstores ###
* Asos
* Bijenkorf
* Camicissima (on hold)
* Clarks
* Douglas
* ICI Paris XL
* MiuMiu
* Prada (on hold)
* Ralph Lauren (on hold)
* Sarenza
* Sephora
* Ted Baker
* Tommy Hilfiger
* Topshop
* Zalando
* Zara

### Personal goal ###
Because of my interest in data crawling and Python, I thought it would be a nice idea to create a Python parser for different web stores. This way I learn how to retrieve information from different types of data, make the data uniform to be put in a database and create proper classes in Python to keep the code clean.

### The things that I have learned and applied currently ###
* Create a base class for the webcrawler and inherit from it for every store
* Use urllib2 and modify the request header to target a country specific page
* Use regular expressions and CSS selectors to find data elements in the page content
* Use Pylint to improve the code quality
* Use Object-relational mappings (ORM) to handle products between Python and the MySQL database