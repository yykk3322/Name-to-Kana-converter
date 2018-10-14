# -*- coding: utf-8 -*-
import os
import sys
import time
import random

if sys.version_info[0] > 2:
    from http.cookiejar import LWPCookieJar
    from urllib.request import Request, urlopen
    from urllib.parse import quote_plus, urlparse, parse_qs
else:
    from cookielib import LWPCookieJar
    from urllib import quote_plus
    from urllib2 import Request, urlopen
    from urlparse import urlparse, parse_qs

# Lazy import of BeautifulSoup.
BeautifulSoup = None
# URL templates to make Google searches.
url_home          = "http://www.google.%(tld)s/"
url_search        = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&btnG=Google+Search&inurl=https"
url_next_page     = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&start=%(start)d&inurl=https"
url_search_num    = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&btnG=Google+Search&inurl=https"
url_next_page_num = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&start=%(start)d&inurl=https"

# Cookie jar. Stored at the user's home folder.
home_folder = os.getenv('HOME')
if not home_folder:
    home_folder = os.getenv('USERHOME')
    if not home_folder:
        home_folder = '.'   # Use the current folder on error.
cookie_jar = LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
try:
    cookie_jar.load()
except Exception:
    pass

# Request the given URL and return the response page, using the cookie jar.
def get_page(url):
    """
    Request the given URL and return the response page, using the cookie jar.

    @type  url: str
    @param url: URL to retrieve.

    @rtype:  str
    @return: Web page retrieved for the given URL.

    @raise IOError: An exception is raised on error.
    @raise urllib2.URLError: An exception is raised on error.
    @raise urllib2.HTTPError: An exception is raised on error.
    """
    request = Request(url)
    request.add_header('User-Agent',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
    cookie_jar.add_cookie_header(request)
    response = urlopen(request)
    cookie_jar.extract_cookies(response, request)
    html = response.read()
    response.close()
    cookie_jar.save()
    return html

def search(query, tld='com', lang='ja', num=10, start=0, stop=None, pause=2.0,
               only_standard=False):
    time.sleep(random.random()+0.5)
     # Lazy import of BeautifulSoup.
     # Try to use BeautifulSoup 4 if available, fall back to 3 otherwise.
    global BeautifulSoup
    if BeautifulSoup is None:
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            from BeautifulSoup import BeautifulSoup
            # Set of hashes for the results found.
            # This is used to avoid repeated results.
    hashes = set()
            # Prepare the search string.
    query = quote_plus(query)
            # Grab the cookie from the home page.
    get_page(url_home % vars())
            # Prepare the URL of the first request.
    if start:
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()
    else:
        if num == 10:
            url = url_search % vars()
        else:
            url = url_search_num % vars()
    html = get_page(url)
    soup = BeautifulSoup(html,"lxml")
    if soup.find(class_="_B5d"):
        anchor = soup.find(class_="_B5d").text
        return [anchor,url]
    else:
        return ["",""]

def output_csv():
    fp = open('output/'+ filename + '/output.csv','a')
    fp.write("固有名詞  日本語 ソース\n")

    f = open('output/'+ filename + '/NERlist.txt', 'r')
    search_list = []
    for line in f:
        search_list.append(line)
    f.close()

    for value in search_list:
        result = search(value)
        print(result)
        fp.write(value.replace('\n','')+"\t"+result[0]+"\t"+result[1]+"\n")
    fp.close()

    print('対訳リストが ' + filename + '_output.csv として出力されました')
