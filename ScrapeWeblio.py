# -*- coding: utf-8 -*-
import os
import codecs
import io

import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup

flag = True

def search_name(name):
    url = "https://www.weblio.jp/content/" + quote(name)
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")

    result = soup.find(class_="Gkjyj")

    if result != None:
        try:
            if flag == True:
                return result.find("a")
            elif flag == False:
                result_list = []
                for x in result.find_all("a"):
                    result_list.append(x.text)
                return "[" + ",".join(result_list) + "]"
        except:
            return ""
    else:
        return ""

def parse_text_file():
    print('解析するテキストのファイル名を入力してください')
    name = input('>>>  ')
    fp = open(name + '_output.csv','a')
    fp.write("原語\t日本語\tソース\n")

    f = open(name + '.txt', 'r')
    search_list = []
    for line in f:
        search_list.append(line)
    f.close()
    print(search_list)

    for x in search_list:
        result = x.replace("\n","") + "\t"
        words = x.split(" ")
        source = []
        for t in words:
            search_name_result = search_name(t)
            result += search_name_result + " "
            if search_name_result != "":
                source.append(("https://www.weblio.jp/content/" + quote(t)).replace("%0A",""))
        result += "\t" + ", ".join(source) +"\n"
        print(result)
        fp.write(result)
    fp.close()

if __name__ == '__main__':
    print('ファイルを簡易解析したい場合は1を、詳細解析したい場合は2を、人名を調べたい場合は3を入力してください')
    select = input('>>>  ')
    if select == "1":
        flag = True
        parse_text_file()
    elif select == "2":
        flag = False
        parse_text_file()
    elif select == "3":
        print('調べたい人名を入力してください')
        name = input('>>>  ')
        print(search_name(name))
