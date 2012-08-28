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
    """
        Pagina de inicio

        por el momento solo tiene contenido estatico que falta rellenar
    """
    mi_template = get_template('index.html')
    dict = generate_base_keys(request)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def login(request):
    """
        Vista de Inicio de session de usuarios
    """
    mi_template = get_template('login.html')
    dict = generate_base_keys(request)

    #dict['user_menu'] = load_cont('not-login-menu.txt')

    if not request.user.is_authenticated():
        dict['not_login'] = True

        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)

            if (user is not None) and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/')

            else:
                dict['login_error'] = True
    else:
        dict['username'] = request.user.username

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def logout(request):
    """
        Vista para cerrar session
    """
    mi_template = get_template('logout.html')
    dict = generate_base_keys(request)

    if request.user.is_authenticated():
        auth.logout(request)
        dict['user_info'] = ACont()
    
    else:
        dict['error'] = True

    
    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def restricted_access(request, area="NULL"):
    """
        Para mostrar la vista de acceso restringido
    """
    mi_template = get_template('restricted-access.html')
    dict = generate_base_keys(request)
    dict['area'] = area
    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def change_password(request):
    """
        Vista para cambiar la contraseña del usuario
    """
    if request.user.is_authenticated():
        mi_template = get_template('change-password.html')
        dict = generate_base_keys(request)

        dict['form'] = my_forms.ChangePasswordForm(auto_id=False)

        if request.method == 'POST':
            dict['query'] = True
            form = my_forms.ChangePasswordForm(request.POST, auto_id=False)
            if form.is_valid():
                if request.user.check_password(form.cleaned_data['old_password']):
                    request.user.set_password(form.cleaned_data['password'])

            else:
                dict['form_e'] = form


        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)
