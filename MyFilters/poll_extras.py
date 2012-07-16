#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Filtros Personalizados
"""

from django import template


register = template.Library()


@register.filter
def testf(value):
    return "HOLA"


#def dict_value(value, argv):
#    return value[argv]



