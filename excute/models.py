# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Hosts(models.Model):
    '''host'''
    pub_ip = models.CharField(max_length=16, unique=True, verbose_name='公网ip')
    inner_ip = models.CharField(max_length=16, unique=True, verbose_name='内网ip')
    status_choices = (
        (0, u'new'),
        (1, u'up'),
        (2, u'cancel'),
        (3, u'known'),
    )
    status = models.PositiveSmallIntegerField(choices=status_choices, default=0, verbose_name='机器状态')
    create_time = models.DateTimeField()
    host_configuration = models.ForeignKey('Configuration')
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    project_name = models.ForeignKey('Project', verbose_name='所属项目')


    def __str__(self):
        return self.inner_ip

    class Meta:
        verbose_name = u'主机表'
        verbose_name_plural = u'主机表'


class Configuration(models.Model):
    '''详细配置'''
    name = models.CharField(max_length=32, verbose_name='配置类型')
    specific_config = models.TextField(verbose_name='配置详情')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'主机配置表'
        verbose_name_plural = u'主机配置表'


class Tags(models.Model):
    '''
    标签信息
    '''
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'标签表'
        verbose_name_plural = u'标签表'


class Project(models.Model):
    '''项目表'''
    name = models.CharField(max_length=16, verbose_name='项目名称')
    note = models.TextField(verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'项目表'
        verbose_name_plural = u'项目表'


class Services(models.Model):
    '''部署服务表'''
    service_num = models.CharField(max_length=64, verbose_name='服务编号', blank=True, null=True)
    # uuid = models.CharField(max_length=64, verbose_name='服务唯一标识', blank=True, null=True)
    type_choices = (
        (0, u'DB'),
        (1, u'Redis'),
        (2, u'Serverlist'),
        (3, u'cobar/mycat'),
        (4, u'GM'),
        (5, u'Sfs'),
        (6, u'api'),
        (7, u'DB_backup'),
        (8, u'other'),
    )
    type = models.PositiveSmallIntegerField(choices=type_choices, verbose_name='服务类型')
    deploy_host = models.ForeignKey('Hosts', verbose_name='所属主机')
    deploy_time = models.DateTimeField(verbose_name='部署时间')
    version = models.CharField(max_length=8, verbose_name='软件版本', blank=True, null=True)
    port = models.IntegerField(verbose_name='服务监听端口', blank=True, null=True)
    dns_name = models.CharField(max_length=128, verbose_name='服务域名',blank=True, null=True)
    use_status_choices = (
        (0, u'备用'),
        (1, u'使用'),
    )
    use_status = models.PositiveSmallIntegerField(choices=use_status_choices, verbose_name='使用状态', default=1)
    flags = models.CharField(max_length=32, blank=True, null=True)
    install_way_choices = (
        (0, u'source'),
        (1, u'yum/rpm'),
        (2, u'docker'),
        (3, u'other'),
    )
    # to_db = models.ForeignKey('self', related_name='uuid', verbose_name='to_db', blank=True, null=True)
    # to_slave_db = models.ForeignKey('self', verbose_name='slave-db', blank=True, null=True)
    install_way = models.PositiveSmallIntegerField(choices=install_way_choices, verbose_name='安装方式')

    def __str__(self):
        return "%s-%s-%s" % (str(self.type), self.port, self.deploy_host)

    class Meta:
        verbose_name = u'部署服务表'
        verbose_name_plural = u'部署服务表'


class DBms(models.Model):
    '''db信息关系表'''
    master = models.ForeignKey(Services, verbose_name='主库')
    slave = models.OneToOneField(Services, related_name='uuid', verbose_name='从库')

    def __str__(self):
        return "%s-%s" % (self.master, self.slave)

    class Meta:
        verbose_name = u'db从主表'
        verbose_name_plural = u'db主从表'


class DBsfs(models.Model):
    '''db sfs信息表'''
    sfs = models.OneToOneField(Services, verbose_name='sfs')
    db = models.ForeignKey(DBms, verbose_name='数据库')

    def __str__(self):
        return "%s-%s" % (self.sfs, self.db)

    class Meta:
        verbose_name = u'sfsdb表'
        verbose_name_plural = u'sfsdb表'
