# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'lyops.settings'
import time
import commands
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from dwebsocket import require_websocket
from models import *
from ansi2html import Ansi2HTMLConverter
from playbooks.ansible_run import *

# Create your views here.
def index(request):
    page = request.GET['page']
    if page == 'host':
        status = request.GET.get('status', '0')
        if status == '4':
            hostlist = Hosts.objects.all().order_by('-create_time')
        else:
            hostlist = Hosts.objects.filter(status=status).order_by('-create_time')
        context = {
            'hostlist': hostlist,
        }
        return render(request, 'excute/host.html', context)
    elif page == 'service':
        type = request.GET['type']
        if type == '-1':
            service_list = Services.objects.all().order_by('-deploy_time')
        else:
            service_list = Services.objects.filter(type=type).order_by('-deploy_time')
        context = {
            'service_list': service_list,
        }
        return render(request, 'excute/service.html', context)

def addhost(request):
    data = json.loads(request.body)
    pub_ip = data['pub_ip']
    inner_ip = data['inner_ip']
    status = data['status']
    project_name = data['project_name']
    create_time = data['create_time']
    host_configuration = data['host_configuration']
    price = data['price']

    host = Hosts()
    host.inner_ip = inner_ip
    host.pub_ip = pub_ip
    host.status = status
    project_name = Project.objects.get(name=project_name)
    host.project_name = project_name
    host.create_time = create_time
    host_configuration = Configuration.objects.get(name=host_configuration)
    host.host_configuration = host_configuration
    host.price = price

    try:
        host.save()
        return JsonResponse({'result': 1})
    except (BaseException), e:
        print e
        return JsonResponse({'result': 0})

def testwsindex(request):
    return render(request, 'excute/websocket_test.html')

@require_websocket
def testws(request):
    conv = Ansi2HTMLConverter(inline=True)

    # message = request.websocket.wait()



    with open('/data/pycharm/python2_base/lyops/excute/playbooks/ansible-3.out', 'r') as f:
        while True:

            ansible_start_pid = commands.getstatusoutput('ps aux|grep ansible_start | grep -v grep')[1]
            if ansible_start_pid:
                while True:

                    content = f.readline()
                    if content:
                        message = b'%s' % content
                        request.websocket.send(conv.convert(message, full=False))
                    else:
                        time.sleep(1)
                        break
            else:
                while True:
                    content = f.readline()
                    if content:
                        message = b'%s' % content
                        request.websocket.send(conv.convert(message, full=False))
                    else:
                        try:
                            request.websocket.send(b'filenull')
                            message = request.websocket.wait()
                        except:
                            break
                break

        # for message in request.websocket:
        #     # f = open('/data/pycharm/python2_base/lyops/playbooks/ansible-3.out', 'r')
        #     request.websocket.send(message)  # 发送消息到客户端
