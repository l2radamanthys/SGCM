#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Filtros Personalizados
"""

from django import template


register = template.Library()


@register.filter
def dict_value(value, argv):
    return value[argv]



