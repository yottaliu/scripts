#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 用于把shadowsocks的配置文件gui-config.json分割成单个节点的配置文件
import sys
import os
import json
if __name__ == '__main__':
    source_file = '/home/yotta/Downloads/gui-config.json'
    target_dir = '/etc/shadowsocks/'
    args = sys.argv
    argc = len(args)
    if argc >= 2:
        source_file = args[1]
    if argc == 3:
        target_dir = args[2]
    with open(source_file, 'r') as fr:
        data = json.load(fr)
    for enum in data['configs']:
        with open(os.path.join(target_dir, enum['server']+'.json'), 'w') as fw:
            json.dump(enum, fw, ensure_ascii=False, indent=4)
