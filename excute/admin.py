# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

# Register your models here.
admin.site.register(Hosts)
admin.site.register(Configuration)
admin.site.register(Services)
admin.site.register(Tags)
admin.site.register(DBms)
admin.site.register(DBsfs)
admin.site.register(Project)