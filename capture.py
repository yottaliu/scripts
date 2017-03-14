#!/usr/bin/env python3
import os
import re
import requests
import pdb
entry = '0014316089557264a6b348958f449949df42a6d3a2e542c000'
base = 'http://www.liaoxuefeng.com'
pattern_css = re.compile(r'.*<link.*href.*=.*".*\.css".*')
pattern_img = re.compile(r'.*<img.*src.*=.*".*".*')
pattern_page = re.compile(r'.*<a.*href.*=.*".*".*')
pattern_start = re.compile(r'<div.*id.*=.*main.*')
def get_page_elem(fname):
    start_css = False
    start_img = False
    fr = open(fname, 'r')
    for line in fr.readlines():
        if '<head' in line:
            start_css = True
        elif '</head' in line:
            start_css = False
        elif '<body' in line:
            start_img = True
        elif '</body' in line:
            start_img = False
        if start_css and re.search(pattern_css, line):
            file_css = line.partition('href')[2].partition('"')[2].partition('"')[0]
            req = requests.get(base + file_css)
            if not os.path.exists(os.path.split('./' + file_css)[0]):
                os.makedirs(os.path.split('./' + file_css)[0])
            if not os.path.isdir('./' + file_css):
                with open('./' + file_css, 'w') as fw:
                    fw.write(req.text)
        if start_img and re.search(pattern_img, line):
            file_img = line.partition('src')[2].partition('"')[2].partition('"')[0]
            if not file_img.startswith('http'):
                req = requests.get(base + file_img)
                if not os.path.exists(os.path.split('./' + file_img)[0]):
                    os.makedirs(os.path.split('./' + file_img)[0])
                if not os.path.isdir('./' + file_img):
                    with open('./' + file_img, 'wb') as fw:
                        fw.write(req.content)
    fr.close()
def get_other_pages(fname):
    # pdb.set_trace()
    stack = -1
    fr = open(fname, 'r')
    for line in fr.readlines():
        if re.search(pattern_start, line):
            stack = 0
        if stack >= 0:
            if '<div' in line and not '</div' in line:
                stack += 1
            if not '<div' in line and '</div' in line:
                stack -= 1
        if stack == 0:
            break
        if stack > 0 and re.search(pattern_page, line):
            file_page = line.partition('href')[2].partition('"')[2].partition('"')[0]
            if not file_page.startswith('javascript:') and not file_page.startswith('http'):
                req = requests.get(base + file_page)
                if os.path.exists(os.path.split('./' + file_page)[0]):
                    if not os.path.isdir(os.path.split('./' + file_page)[0]):
                        os.rename(os.path.split('./' + file_page)[0], os.path.join(os.path.split(os.path.split('.' + file_page)[0])[0], 'index.html'))
                        os.makedirs(os.path.split('./' + file_page)[0])
                else:
                    os.makedirs(os.path.split('./' + file_page)[0])
                if not os.path.isdir('./' + file_page):
                    with open('./' + file_page, 'w') as fw:
                        fw.write(req.text)
                    get_page_elem('./' + file_page)
    fr.close()
if __name__ == '__main__':
    get_page_elem(entry)
    get_other_pages(entry)
