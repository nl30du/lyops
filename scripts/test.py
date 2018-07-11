#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands


def checkUser(ip, username):
    status, output = commands.getstatusoutput("ssh -o PubkeyAuthentication=no -o StrictHostKeyChecking=no root@{} 'id {}'".format(ip, username))
    print status, output


checkUser('192.168.146.133', 'tangchengwei')
