# -*- coding: utf-8 -*-
import os
import codecs
import io

import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup

def search_name(name):
    url = "https://www.weblio.jp/content/" + quote(name)
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")

    result = soup.find(class_="Gkjyj").find("a").text
    print(result)

if __name__ == '__main__':
    print('調べたい人名を入力してください')
    name = input('>>>  ')
    search_name(name)
