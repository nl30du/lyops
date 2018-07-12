# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import auth
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from models import  *
from scripts.modify_user import *


@login_required
def index(request):

    return render(request, 'ops/index.html')


def login(request):
    return render(request, 'ops/login.html')


@login_required
def change(request):
    return render(request, 'ops/change.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/ops/login/')


def handle_login(request):
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)
    if user and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/ops/')

    else:
        return HttpResponseRedirect('/ops/login/?result=0')


@login_required
def handle_change(request):
    username = request.user
    password = request.POST['oldpassword']
    newpassword = request.POST['newpassword']
    user = auth.authenticate(username=username, password=password)

    if user:
        user.set_password(newpassword)
        user.save()
        auth.login(request, user)
        return render(request, 'ops/change_succeeded.html')
    else:
        return HttpResponse('ops/change_failed.html')


@login_required
def check_password(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user and user.is_active:
        context = {
            'status_code': 1,
        }
    else:
        context = {
            'status_code': 0,
        }

    return JsonResponse(context)


@login_required
def userlist(request):
    project_list = Project.objects.all()
    user_list = OpsUserProfile.objects.all().order_by('-id')

    context = {
        'user_list': user_list,
        'project_list': project_list,
    }
    return render(request, 'ops/userlist.html', context)


@login_required
def duser(request):
    username = request.POST['username']
    user = OpsUserProfile.objects.get(name=username)
    project_list = [ (x.lander, x.password) for x in user.project.all() ]
    for item in project_list:
        host = InitUser(item[0], 'root', item[1], 22)
        res = host.checkuser_inhost(username)
        if res == 1:
            host.del_user(username)
    user.delete()
    return JsonResponse({'status': 1})


@login_required
def copykey(request):
    username = request.POST['username']
    project_name = request.POST['project_name']
    user = OpsUserProfile.objects.get(name=username)
    project = Project.objects.get(name=project_name)
    old_ip = user.project.all()[0].lander
    old_password = user.project.all()[0].password
    new_ip = project.lander
    new_password = project.password
    old_host = InitUser(old_ip, 'root', old_password, 22)
    old_host.syncfiles(0, '/home/{}/.ssh/id_rsa'.format(username), 'id_rsa')

    new_host = InitUser(new_ip, 'root', new_password, 22)
    res = new_host.checkuser_inhost(username)
    plist = [x.name for x in user.project.all()]
    if project_name not in plist:
        user.project.add(project)
    res_info = {}

    if res == 1:
        new_host.syncfiles(1, 'id_rsa', '/home/{}/.ssh/id_rsa'.format(username))
        new_host.correct(username)
        res_info = {
            'status': 1,
        }
    elif res == 0:
        new_host.modify_user(username, user.password)
        new_host.syncfiles(1, 'id_rsa', '/home/{}/.ssh/id_rsa'.format(username))
        new_host.correct(username)
        res_info = {
            'status': 1,
        }

    return JsonResponse(res_info)


@login_required
def adduser(request):
    project_list = Project.objects.all()
    context = {
        'project_list': project_list,
    }
    return render(request, 'ops/adduser.html', context)


@login_required
def deluser(request):
    pass


@login_required
def syncuser(request):
    pass


@login_required
def handle_useradd(request):
    # InitUser
    username = request.POST['username']
    project_name = request.POST['project_name']
    usertype = request.POST['usertype']

    lander = Project.objects.get(name=project_name)
    lander_host = lander.lander
    lander_password = lander.password
    lander_host = InitUser(lander_host, 'root', lander_password, 22)
    res = lander_host.checkuser_indb(username)
    if res == 0:
        info = lander_host.adduser(username)
        user = OpsUserProfile()
        user.name = info['username']
        user.password = info['password']
        user.public_key = info['pub_key']
        user.fingerprint = info['fingerprint']
        user.login_user = int(usertype)
        user.save()
        user.project.add(lander)

        return_res = {
            'status': 1,
            'user_name': info['username'],
            'password': info['password'],
        }
        return JsonResponse(return_res)
    else:
        return JsonResponse({'status': 0})


@login_required
def manager(request):

    project_list = Project.objects.all()
    context = {
        'project_list': project_list,
        'request': request,
    }
    return render(request, 'ops/manager.html', context)


@login_required
def manager_modify(request):
    if request.method == 'GET':
        id = request.GET['id']
        mode = request.GET['mode']
        project = Project.objects.filter(pk=id)

        if project and mode == 'del':
            project[0].delete()
            res = {
                'status': 'ok',
            }
        return JsonResponse(res)

    elif request.method == 'POST':
        project_name = request.POST['project_name']
        lander = request.POST['lander']
        password = request.POST['password']
        key = 'nouse'
        project = Project()
        project.name = project_name
        project.lander = lander
        project.password = password
        project.pem = key
        project.save()

        return HttpResponseRedirect('/ops/manager/')


@login_required
def check_project(request):
    project_name = request.POST['project_name']
    lander = request.POST['lander']
    project = Project.objects.filter(name=project_name, lander=lander)
    if project:
        return JsonResponse({'exist': 1})
    else:
        return JsonResponse({'exist': 0})


@login_required
def commandlist(request):
    page_index = request.GET['index']
    command_list = CmdTrack.objects.all().order_by('-id')
    p = Paginator(command_list, 14)
    page_list = p.page(page_index)
    page_number = p.num_pages

    check = True


    if int(page_index) < 9:
        page_list_show = range(1, 16)
    elif int(page_index) >= 9 and int(page_index) < page_number-9:
        page_list_show = range(int(page_index)-7, int(page_index)+8)

    else:
        page_list_show = range(page_number-15, page_number+1)
        check = False


    context = {
        'command_list': command_list,
        'page_index': page_index,
        'page_list': page_list,
        'request': request,
        'page_list_show': page_list_show,
        'check': check,
    }
    return render(request, 'ops/commandlist.html', context)


def sshkey(request):
    fingerprint = request.GET['fp']
    loginuser = request.GET['loginuser']
    project_name = request.GET['p']
    user = OpsUserProfile.objects.get(fingerprint=fingerprint)
    loginuser_db = user.get_login_user_display()
    plist = [ x.name for x in user.project.all() ]
    if loginuser_db == loginuser and project_name in plist:
        res_str = "command=\"/sbin/prelogin.sh {}\" {}".format(user.name, user.public_key)
    else:
        res_str = ''

    return HttpResponse(res_str)
