""" samples/crawl_02.py """
################################################################################
# Application:      WebParser example 02
# File:             samples/crawl_01.py
# Goal:             Retrieve content when JavaScript is used in page
# Input:
# Output:
# Example:
#
# History:          2016-06-27 - JJ     Creation of the file
#
################################################################################

################################################################################
# Imports
################################################################################
import lxml.html
import urllib2

from pyvirtualdisplay import Display
from selenium import webdriver

################################################################################
# Definitions
################################################################################
HEADER = {'Accept-Language': 'nl-NL',
          'User-Agent': """Mozilla/5.0 (Windows; U;
                                    Windows NT 6.1;
                                    nl-NL;
                                    rv:1.9.1.5)
                       Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729);
                       nl-NL"""}
################################################################################
# Classes
################################################################################
class WebParser(object):
    """ Definition of the WebParser """
    def __init__(self, *args, **kwargs):
        """ Initialize the WebParser """
        super(WebParser, self).__init__(*args, **kwargs)

    @staticmethod
    def parse_page(url):
        """ Open URL and return the element tree of the page """
        display = Display(visible=0, size=(1920, 1080))
        display.start()
        browser = webdriver.Firefox()
        browser.get(url)
        data = browser.page_source
        tree = lxml.html.fromstring(data)
        browser.quit()
        display.stop()
        return tree

    @staticmethod
    def find_css_element(etree, element):
        """ Find an element in the element tree and return it """
        return etree.cssselect(element)

################################################################################
# Functions
################################################################################
def main():
    """ Main function """
    parser = WebParser()
    etree = parser.parse_page('http://isitweekendalready.com')
    divs = parser.find_css_element(etree, '#result')
    print divs[0].text.strip()

################################################################################
# main
################################################################################
if __name__ == "__main__":
    main()
