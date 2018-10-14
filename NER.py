# -*- coding: utf-8 -*-
import os
import codecs
import io

from corenlp import batch_parse
import GoogleResultScraper

def extract_NER():
    print('テキストを解析するディレクトリの名前を入力してください')
    filename = input('>>>  ')
    print('固有名詞の抽出を開始します')
    corenlp_dir = "/usr/local/lib/stanford-corenlp-full-2017-06-09/"
    # corenlp_dir = "stanford-corenlp-full-2017-06-09/"
    raw_text_directory = "output/sf"
    properties_file = "user.properties"
    parsed = batch_parse(raw_text_directory, corenlp_dir)
    NERlist = [];
    preTag = ""
    currentNER = ""
    TempTag = ""
    count = 0
    for value in parsed:
        count += 1
        valuePh = value['sentences']
        for value2 in valuePh:
            value2Ph = value2['words']
            for value3 in value2Ph:
                value4 = value3[1]
                tempTag = value4['NamedEntityTag']
                if not tempTag == preTag and not currentNER == "":
                    NERlist.append(currentNER)
                    currentNER = ""
                if value4['NamedEntityTag'] == 'PERSON' or value4['NamedEntityTag'] == 'ORGANIZATION' or value4['NamedEntityTag'] == 'LOCATION':
                    if currentNER == "":
                        currentNER = currentNER + value3[0]
                    else:
                        currentNER = currentNER + ' ' + value3[0]
                preTag = value4['NamedEntityTag']

                print(value3[0])
                print(value4['NamedEntityTag'])
        NERlist.append(currentNER)
    NERlist_uniq = []
    for x in NERlist:
        if x not in NERlist_uniq:
            NERlist_uniq.append(x)
    fp = open('output/'+ filename +'/NERlist.txt','a')
    for value in NERlist_uniq:
        fp.write(value+"\n")
    fp.close()
    print('固有名詞リストが' + filename + '/NERlist.txt として出力されました')

if __name__ == '__main__':
    extract_NER()
