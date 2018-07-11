# -*- coding: utf-8 -*-

import random
import paramiko
from .. import models


class RemoteExcute(object):

    def __init__(self, hostname, username, password, port):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port

    def connect(self, connect_type):
        if connect_type == 'cmd':
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(self.hostname, self.port, self.username, self.password)
            self.ssh_client = ssh_client
        elif connect_type == 'transfile':
            ssh_client = paramiko.Transport((self.hostname, self.port))
            ssh_client.connect(username=self.username, password=self.password)
            ssh_sftp = paramiko.SFTPClient.from_transport(ssh_client)
            self.ssh_sftp = ssh_sftp

    def excute(self, cmd):
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        return stdout.readlines()

    def copy(self, copy_type, path1, path2):
        if copy_type == 0:
            self.ssh_sftp.get(path1, path2)
        elif copy_type == 1:
            self.ssh_sftp.put(path1, path2)

    def todest(self, lpath_file, dpath_file):
        self.ssh_sftp.put(lpath_file, dpath_file)


class InitUser(RemoteExcute):

    def __init__(self, hostname, username, password, port):
        super(InitUser, self).__init__(hostname, username, password, port)

    def checkuser_inhost(self, username):
        self.connect('cmd')
        res = self.excute('id {}'.format(username))
        if res:
            return 1
        else:
            return 0

    def checkuser_indb(self, username):
        user = models.OpsUserProfile.objects.filter(name=username)
        if user:
            return 1
        else:
            return 0

    def adduser(self, username):
        self.connect('cmd')
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
        fingerprint = self.excute("ssh-keygen -lf /home/%s/.ssh/id_rsa | awk '{print $2}'" % username)
        pub_key = self.excute("cat /home/{}/.ssh/id_rsa.pub".format(username))
        info['password'] = password_str
        info['fingerprint'] = fingerprint[0].strip('\n')

        info['pub_key'] = pub_key[0].strip('\n')

        self.ssh_client.close()
        return info

    def del_user(self, username):
        self.connect('cmd')
        self.excute("pkill -KILL -u {}".format(username))
        self.excute("cp -R /home/{} /home/{}-`date '+%Y%m%d%H%M'` && userdel -r {}".format(username, username, username, username))
        self.ssh_client.close()

    def modify_user(self, username, password):
        self.connect('cmd')
        self.excute("useradd {} && echo '{}' | passwd --stdin {}".format(username, password, username))
        self.excute("mkdir /home/{}/.ssh/ && chown 700 /home/{}/.ssh && chown -R {}.{} /home/{}/".format(username, username, username, username, username))
        self.ssh_client.close()

    def correct(self, username):
        self.connect('cmd')
        self.excute("chown -R {}.{} /home/{}/.ssh/id_rsa && chmod 600 /home/{}/.ssh/id_rsa".format(username, username, username, username))
        self.ssh_client.close()

    def syncfiles(self, copy_type, path1, path2):
        self.connect('transfile')
        self.copy(copy_type, path1, path2)


if __name__ == "__main__":
    a = InitUser('192.168.146.130', 'root', 'centos', 22)
    res = a.checkuser_inhost('tangchengwei')
    if res == 1:
        a.del_user('tangchengwei')
        # a.syncfiles(0, '/home/laodong/.ssh/id_rsa', 'id_rsa')
        # a.syncfiles(1, 'hehe.log', '/tmp/hehe.log')

    elif res == 0:
        # a.adduser('laodong')
        pass


