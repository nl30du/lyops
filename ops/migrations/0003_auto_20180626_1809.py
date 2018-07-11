# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-26 18:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0002_cmdtrack'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='lander',
            field=models.CharField(default='1.1.1.1', max_length=32, unique=True, verbose_name='\u4e2d\u63a7\u673a'),
        ),
        migrations.AddField(
            model_name='project',
            name='password',
            field=models.CharField(default='1.1.1.1', max_length=255, verbose_name='\u4e2d\u63a7\u673a\u5bc6\u7801'),
        ),
        migrations.AddField(
            model_name='project',
            name='pem',
            field=models.TextField(default='1.1.1.1', verbose_name='\u4e2d\u63a7\u673a\u79d8\u94a5'),
        ),
    ]