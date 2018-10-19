# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.testwsindex, name='index'),
    url(r'addhost/$', views.addhost, name='addhost'),
    url(r'testws/$', views.testws, name='testws'),
]
