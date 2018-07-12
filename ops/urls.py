# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'handle_login/$', views.handle_login, name='handle_login'),
    url(r'login/$', views.login, name='login'),
    url(r'handle_change/$', views.handle_change, name='handle_change'),
    url(r'check_password/$', views.check_password, name='check_password'),
    url(r'change/$', views.change, name='change'),

    url(r'userlist/copykey/$', views.copykey, name='copykey'),
    url(r'userlist/duser/$', views.duser, name='duser'),
    url(r'userlist/$', views.userlist, name='userlist'),
    url(r'adduser/handle_useradd/$', views.handle_useradd, name='handle_useradd'),
    url(r'adduser/$', views.adduser, name='adduser'),
    url(r'manager/check_project/$', views.check_project, name='check_project'),
    url(r'manager_modify/$', views.manager_modify, name='manager_modify'),
    url(r'manager/$', views.manager, name='manager'),
    url(r'commandlist/$', views.commandlist, name='commandlist'),
    url(r'sshkey/', views.sshkey, name='sshkey'),

]
