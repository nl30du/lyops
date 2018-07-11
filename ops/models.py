# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


# Create your models here.
class OpsUserProfile(models.Model):
    ''''''
    name = models.CharField(max_length=32, verbose_name='用户名')
    vname = models.CharField(max_length=32, verbose_name='详细名称', blank=True, null=True)
    password = models.CharField(max_length=32, verbose_name='密码')
    public_key = models.TextField(verbose_name='用户公钥')
    fingerprint = models.CharField(max_length=64, verbose_name='秘钥指纹')
    login_user_choices = (
        (0, u'root'),
        (1, u'common'),
    )
    login_user = models.PositiveSmallIntegerField(choices=login_user_choices, verbose_name='登录用户', default=1)
    project = models.ManyToManyField('Project', verbose_name='所属项目')
    islimited_choices = (
        (0, u'status1'),
        (1, u'status2'),
        (2, u'status3'),
    )
    islimited = models.PositiveSmallIntegerField(choices=islimited_choices, default=0)

    def __str__(self):
        return '{}-{}'.format(self.pk, self.name)

    class Meta:
        verbose_name = '认证用户表'
        verbose_name_plural = '认证用户表'


class Project(models.Model):
    ''''''
    name = models.CharField(max_length=32, verbose_name='项目名称')
    vname = models.CharField(max_length=32, verbose_name='详细项目名称', blank=True, null=True)
    lander = models.CharField(max_length=32, verbose_name='中控机')
    password = models.CharField(max_length=255, verbose_name='中控机密码')
    pem = models.TextField(verbose_name='中控机秘钥')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        unique_together = ('name', 'lander')
        verbose_name = '项目表'
        verbose_name_plural = '项目表'


class UserProfile(AbstractUser):
    '''
    账户表，扩展django自带的User表
    '''
    # name = models.CharField(max_length=32, verbose_name=u'用户名')
    roles = models.CharField(max_length=10, verbose_name='角色', blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = u'账户表'
        verbose_name_plural = u'账户表'


class CmdTrack(models.Model):
    host = models.CharField(max_length=15, db_index=True)
    loginuser = models.CharField(max_length=512, blank=True, null=True)
    realuser = models.CharField(max_length=512, blank=True, null=True)
    fromip = models.CharField(max_length=15, blank=True, null=True)
    logintime = models.DateTimeField()
    logintype = models.IntegerField(default=0)
    command = models.CharField(max_length=1024, blank=True, null=True)

