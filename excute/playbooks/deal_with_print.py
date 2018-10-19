#!/usr/bin/env python
# -*- coding: utf-8 -*-

def printinfo(modules, result_data, res):
    if res == 'unreachable':
        # print result_data._host.get_name(), result_data._result
        print '\033[1;31m%s | UNREACHABLE! => {' % result_data._host.get_name()
        for key, val in result_data._result.items():
            print '    \"%s\": %s' % (key, str(val).strip('\r\n'))
        print '}\033[0m\n'

    elif res == 'ok':
        if modules == 'shell':
            print '\033[0;32m%s | SUCCESS | rc=0 >>\033[0m' % result_data._host.get_name()
            # print result_data._host.get_name(), result_data._result
            cmd_res = result_data._result
            cmd_res = cmd_res['stdout'].split('\n')
            for line in cmd_res:
                print '\033[0;32m' + line + '\033[0m'
        elif modules == 'ping':
            print '\033[0;32m%s | SUCCESS => {' % result_data._host.get_name()
            cmd_res = result_data._result
            print "    \"changed\": %s," % cmd_res['changed']
            print "    \"ping\": \"%s\"" % cmd_res['ping']
            print '}\033[0m\n'

    elif res == 'failed':
        print '\033[0;31m%s | FAILED | rc=2 >>\033[0m' % result_data._host.get_name()
        cmd_res = result_data._result
        print '\033[0;31m' + cmd_res['stdout'] + cmd_res['stderr'] + '\n\033[0m'