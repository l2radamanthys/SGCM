#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth #para login
from django.contrib.auth.models import User

import GestionTurnos.forms as my_forms
from utils import *
from globals import *




def register(request):
    """
        Metodo para registrar un nuevo usuario
    """
    mi_template = get_template('GestionTurnos/usuario-nuevo.html')
    dict = generate_base_keys(request)

    if not request.user.is_authenticated():
        dict['user_menu'] = load_cont('not-login-menu.txt')

        dict['show_form'] = True
        dict['form'] = my_forms.RegisterForm()
        
    else:
        dict['user_menu'] = load_cont('paciente-menu.txt')
        pass


    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)