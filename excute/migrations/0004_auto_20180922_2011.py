# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-09-22 20:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('excute', '0003_auto_20180922_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dbms',
            name='slave',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='uuid', to='excute.Services', verbose_name='\u4ece\u5e93'),
        ),
    ]