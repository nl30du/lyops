# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-27 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0006_opsuserprofile_islimited'),
    ]

    operations = [
        migrations.AddField(
            model_name='opsuserprofile',
            name='password',
            field=models.CharField(default='sdfsdfds', max_length=32, verbose_name='\u5bc6\u7801'),
        ),
    ]
