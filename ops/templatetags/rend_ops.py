# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
# from ops.models import *
from django import template
import importlib

register = template.Library()

@register.simple_tag
def subtract_oblist(attr1, attr2):
    res = attr1 - attr2
    return res


