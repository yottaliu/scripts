#!/usr/bin/env python3
# 用于把shadowsocks的配置文件gui-config.json分割成单个节点的配置文件
fr = open('/home/yotta/Downloads/gui-config.json', 'r')
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
            with open('/etc/shadowsocks/' + fname, 'w') as fw:
                fw.write(tmp)
            tmp = ''
        else:
            if line.strip().startswith('"server":') or line.strip().startswith('server:'):
                fname = line.strip().rpartition(':')[2].partition('"')[2].rpartition('"')[0] + '.json'
            tmp += '    ' + line.lstrip()
fr.close()
