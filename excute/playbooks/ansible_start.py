#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from ansible_run import *

'''
以此中方式给定主机列表，默认执行主机组为 default_group
resource = [
    {
        "hostname": "172.20.3.31", "port": "22", "username": "root", "password": "password", "ip": '172.20.3.31'
    },
]
'''

def task_run(hostname, port=22, username='root'):
    pass

# 自定义主机组，并给定对应主机和组变量
resource = {
    'test': {
        'hosts': [
            {"hostname": "192.168.146.131", "port": "22", "username": "root", "password": "centos",
             "ip": '192.168.146.131',
             'vars': {
                 'style': 'server',
                 'role': 'main',
                 'subordinate': '41',
             }
             },
            {"hostname": "192.168.146.132", "port": "22", "username": "root", "password": "centos",
             "ip": '192.168.146.132',
             'vars': {
                 'style': 'instance',
                 'role': 'subordinate',
                 'subordinate': '41',
             }
             },
        ],
        'vars': {"testvar1": 'aa', "testvar2": 'bb'}
    }
}

interface = AnsiInterface(resource)
# print "copy: ", interface.copy_file(['172.20.3.18', '172.20.3.31'], src='/Users/majing/test1.py', dest='/opt')
# result_data = interface.exec_shell(['192.168.146.131', '192.168.146.132'], 'ls /root/a.txt')
# print result_data


with open('ansible-3.out', 'w') as f:
    stdout_old = sys.stdout
    sys.stdout = f
    sys.stderr = f
    res = interface.exec_playbook()
    sys.stdout = stdout_old

print res
# print res_1['failed']['192.168.146.131']
