#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth #para login
from django.contrib.auth.models import User




import my_forms
from utils import *
from globals import *


def index(request):
    mi_template = get_template('index.html')
    dict = generate_base_keys(request)
    #dict['user_name'] = 'OFFLINE'
    dict['user_menu'] = load_cont('not-login-menu.txt')
    
    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)


def login(request):
    mi_template = get_template('login.html')
    dict = generate_base_keys(request)
    
    dict['style'] += make_css_tag('/media/css/win-style.css')
    dict['style'] += make_css_tag('/media/css/fancy-botons-style.css')



    dict['user_menu'] = load_cont('not-login-menu.txt')

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)