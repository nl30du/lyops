# -*- coding: utf-8 -*-

import random
import paramiko


class RemoteExcute(object):

    def __init__(self, hostname, username, password, port):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port

    def connect(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(self.hostname, self.port, self.username, self.password)
        self.ssh_client = ssh_client

    def excute(self, cmd):
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        return stdout.readlines()


class InitUser(RemoteExcute):

    def __init__(self, hostname, username, password, port):
        super(InitUser, self).__init__(hostname, username, password, port)

    def checkuser(self, username):
        self.connect()
        res = self.excute('id {}'.format(username))
        if res:
            return 1
        else:
            return 0

    def adduser(self, username):

        info = {
            'username': username,
        }

        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
        sa = []
        for i in range(16):
            sa.append(random.choice(seed))
        password_str = ''.join(sa)

        self.excute("useradd {} && echo '{}' | passwd --stdin {}".format(username, password_str, username))
        cmd_str = "\"ssh-keygen -t rsa -b 2048 -N '' -f ~/.ssh/id_rsa\""
        self.excute("su - {} -c {}".format(username, cmd_str))
        fingerprint = self.excute("ssh-keygen -lf /home/{}/.ssh/id_rsa | awk '{print $2}'".format(username))
        pub_key = self.excute("cat /home/{}/.ssh/id_rsa.pub".format(username))

        info['password'] = password_str
        info['fingerprint'] = fingerprint[0].strip('\n')
        info['pub_key'] = pub_key[0].strip('\n')
        return info



if __name__ == "__main__":
    a = InitUser('192.168.146.130', 'root', 'centos', 22)
    res = a.checkuser('tangchengwei')
    if res == 0:
        print a.adduser('tangchengwei')


