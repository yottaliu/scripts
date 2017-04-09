#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import requests
entry = '0014316089557264a6b348958f449949df42a6d3a2e542c000'
base = 'http://www.liaoxuefeng.com'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36',
    'Accept':'text/html;q=0.9,*/*;q=0.8',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding':'gzip',
    'Connection':'close',
    'Referer':None #如果依然不能抓取的话，这里可以设置抓取网站的host
}
pattern_css = re.compile(r'.*<link.*href.*=.*".*\.css".*')
pattern_img = re.compile(r'.*<img.*src.*=.*".*".*')
pattern_page = re.compile(r'.*<a.*href.*=.*".*".*')
pattern_start = re.compile(r'<div.*id.*=.*main.*')
exist_files = set([])
summary = {}
def log(t, name):
    if t == 'directory':
        print('Making directory:', name)
    elif t == 'rename':
        print('Rename from %s to %s' % name)
    else:
        print('Downloading', t, 'file:', name, '...');
        if t in summary:
            summary[t] += 1
        else:
            summary[t] = 0
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
            if file_css not in exist_files:
                req = requests.get(base + file_css, headers = headers)
                exist_files.add(file_css)
                directory = os.path.relpath(os.path.dirname('./' + file_css))
                if not os.path.exists(directory):
                    log('directory', directory)
                    os.makedirs(directory)
                if not os.path.isdir('./' + file_css):
                    log('css', file_css)
                    with open('./' + file_css, 'w') as fw:
                        fw.write(req.text)
        if start_img and re.search(pattern_img, line):
            file_img = line.partition('src')[2].partition('"')[2].partition('"')[0]
            if file_img not in exist_files and not file_img.startswith('http'):
                req = requests.get(base + file_img, headers = headers)
                exist_files.add(file_img)
                directory = os.path.relpath(os.path.dirname('./' + file_img))
                if not os.path.exists(directory):
                    log('directory', directory)
                    os.makedirs(directory)
                if not os.path.isdir('./' + file_img):
                    log('img', file_img)
                    with open('./' + file_img, 'wb') as fw:
                        fw.write(req.content)
    fr.close()
def get_all_pages(fname):
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
            if file_page not in exist_files and not file_page.startswith('javascript:') and not file_page.startswith('http'):
                req = requests.get(base + file_page, headers = headers)
                exist_files.add(file_page)
                directory = os.path.relpath(os.path.dirname('./' + file_page))
                if os.path.exists(directory):
                    if not os.path.isdir(directory):
                        new_name = os.path.join(os.path.dirname(os.path.dirname('.' + file_page)), 'index.html')
                        log('rename', (directory, new_name))
                        os.rename(directory, new_name)
                        log('directory', directory)
                        os.makedirs(directory)
                else:
                    log('directory', directory)
                    os.makedirs(directory)
                if not os.path.isdir('./' + file_page):
                    log('page', file_page)
                    with open('./' + file_page, 'w') as fw:
                        fw.write(req.text)
                    get_page_elem('./' + file_page)
    fr.close()
if __name__ == '__main__':
    req = requests.get(base + '/wiki/' + entry, headers = headers)
    log('page', entry)
    with open('./' + entry, 'w') as fw:
        fw.write(req.text)
    get_all_pages(entry)
    print('Done!')
    print('Total:')
    for t in summary:
        print(summary[t], t)
