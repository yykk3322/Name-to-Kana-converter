# -*- coding: utf-8 -*-
import os
import codecs
import io

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

def pdf_to_txt():
    print('解析するpdfのファイル名を入力してください')
    filename = input('>>>  ')
    print(filename + " を処理中です...")

    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(filename, 'rb')
    filename = filename.replace('.pdf','')
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    count = 0
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        interpreter.process_page(page)
        text = retstr.getvalue()
        text = text.replace('-\n','')
        opfp = open('output/' + filename + "/" + "{0:03d}".format(count)+'_output.txt','a')
        opfp.write(text)
        opfp.close()
        retstr.close()
        retstr = io.StringIO()
        count = count + 1

    text = retstr.getvalue()
    text = text.replace('-\n','')

    device.close()
    retstr.close()
    print('解析結果が ' + filename + '/output.txt として出力されました')
