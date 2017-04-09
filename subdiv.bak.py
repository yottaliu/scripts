#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 用于把shadowsocks的配置文件gui-config.json分割成单个节点的配置文件
# 格式：subdiv.py source_file target_dir
import sys
import os
if __name__ == '__main__':
    source_file = '/home/yotta/Downloads/gui-config.json'
    target_dir = '/etc/shadowsocks/'
    args = sys.argv
    param_count = len(args)
    if param_count >= 2:
        source_file = args[1]
    if param_count == 3:
        target_dir = args[2]
    fr = open(source_file, 'r')
    start = False
    fname = ''
    tmp = ''
    for line in fr.readlines():
        if '[' in line:
            start = True
        if start:
            if line.strip().startswith('{'):
                tmp = '{\n'
            elif line.strip().startswith('}'):
                tmp += '}\n'
                with open(os.path.join(target_dir, fname), 'w') as fw:
                    fw.write(tmp)
                tmp = ''
            else:
                if line.strip().startswith('"server":') or line.strip().startswith('server:'):
                    fname = line.strip().rpartition(':')[2].partition('"')[2].rpartition('"')[0] + '.json'
                tmp += '    ' + line.lstrip()
    fr.close()
