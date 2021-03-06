#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from ansible_api import AnsibleAPI


class AnsiInterface(AnsibleAPI):
    def __init__(self, resource, *args, **kwargs):
        super(AnsiInterface, self).__init__(resource, *args, **kwargs)

    @staticmethod
    def deal_result(info):
        host_ips = info.get('success').keys()
        info['success'] = host_ips

        error_ips = info.get('failed')
        error_msg = {}
        for key, value in error_ips .items():
            temp = {}
            try:
                temp[key] = value[1] + " => " + value[0].get('stderr')
            except:
                pass
            error_msg.update(temp)
        info['failed'] = error_msg
        return info

    def copy_file(self, host_list, src=None, dest=None):
        """
        copy file
        """
        module_args = "src=%s  dest=%s"%(src, dest)
        self.run(host_list, 'copy', module_args)
        result = self.get_result()
        return self.deal_result(result)

    def exec_command(self, host_list, cmds):
        """
        commands
        """
        self.run(host_list, 'command', cmds)
        # result = self.get_result()
        # return result

    def exec_shell(self, host_list, cmds):
        """
        shell
        """
        self.run(host_list, 'shell', cmds)
        result = self.get_result()
        return self.deal_result(result)

    def exec_ping(self, host_list, cmds):
        """
        ping
        """
        self.run(host_list, 'ping', cmds)
        result = self.get_result()
        return self.deal_result(result)

    def exec_script(self, host_list, path):
        """
        在远程主机执行shell命令或者.sh脚本
        """
        self.run(host_list, 'shell', path)
        result = self.get_result()
        return self.deal_result(result)

    def exec_playbook(self):
        self.run_playbook()
        result = self.get_result()
        return self.deal_result(result)


if __name__ == "__main__":
    #resource = [{"hostname": "X.X.X.X", "port": "29157", "username": "root", "password": "password", "ip": 'X.X.X.X'},
    #            {"hostname": "172.20.3.31", "port": "22", "username": "root", "password": "password", "ip": '172.20.3.31'}]

    resource = {
        'test': {
            'hosts': [
                {"hostname": "192.168.146.131", "port": "22", "username": "root", "password": "centos", "ip": '192.168.146.131',
                   'vars': {
                       'style': 'server',
                       'role': 'master',
                       'slave': '41',
                    }
                },
                {"hostname": "192.168.146.132", "port": "22", "username": "root", "password": "centos",
                   "ip": '192.168.146.132',
                   'vars': {
                       'style': 'instance',
                       'role': 'slave',
                       'slave': '41',
                    }
                },
            ],
            'vars': {"testvar1": 'aa', "testvar2": 'bb'}
        }
    }

    interface = AnsiInterface(resource)
    #print "copy: ", interface.copy_file(['172.20.3.18', '172.20.3.31'], src='/Users/majing/test1.py', dest='/opt')
    result_data = interface.exec_shell(['192.168.146.131', '192.168.146.132'], 'ls /root/a.txt')
    print result_data

    # result_data = interface.exec_ping(['192.168.146.131', '192.168.146.132'], '')
    # print result_data

    # for key, val in result_data.items():
    #     for i, j in val.items():
    #         if key != 'unreachable':
    #             # print "\033[0;32mtest \033[0m"
    #             if len(j['stderr']) == 0:
    #                 color = 32
    #             else:
    #                 color = 31
    #             print "\033[0;%dm%s | %s >>\033[0m" % (color, i, key)
    #             print "\033[0;%dm" % color + j['stdout'] + "\033[0m"
    #             print "\033[0;%dm" % color + j['stderr'] + "\033[0m"
    #         else:
    #             print "\033[1;31m%s | %s! => {\033[0m" % (i, key)
    #             print "\033[1;31m    \"changed\": false,\n    \"msg\": \"%s\",\n    \"unreachable\": true\033[0m" % j.strip("\r\n")
    #             print "\033[1;31m}\n\033[0m"
    #         print


    # res_1 = interface.exec_playbook(['192.168.1.41', '192.168.1.44', '192.168.1.45'])
    # print res_1['failed']['192.168.146.131']

    # print "shell: ", interface.exec_script(['172.20.3.18', '172.20.3.31'], 'chdir=/home ls')
    #print "shell: ", interface.exec_script(['172.20.3.18', '172.20.3.31'], 'sh /opt/test.sh')
