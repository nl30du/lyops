# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import auth
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json
from models import *


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