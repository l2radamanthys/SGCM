#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime

from globals import MI_TEMPLATE_DIR, GET, POST



def load_cont(path):
    """
        Carga Contenido desde un archivo de texto
    """
    data = open(os.path.join(MI_TEMPLATE_DIR, path)).readlines()
    cont = ""
    for line in data:
        cont += line
    return cont


def user_menu(request):
    """
        carga el menu de acuerdo al tipo de usuario
    """
    if request.user.is_authenticated():
        group_name = request.user.groups.all()[0].name
        #usuarios
        if group_name == "Pacientes":
            return load_cont(os.path.join('Menu','pacient.txt'))
        #medicos
        elif group_name == "Medicos":
            return load_cont(os.path.join('Menu','medic.txt'))
        #administradores
        else:
            return load_cont(os.path.join('Menu','medic.txt'))
    else:
        return load_cont(os.path.join('Menu','not-login.txt'))



def user_info(request):
    if request.user.is_authenticated():
        return request.user.username
    else:
        return "Usuario no Conectado"



def generate_base_keys(request):
    """
        Genera el dicionario con contenido basico.
    """
    dict = {
        'user_menu': user_menu(request),
        'login_username': user_info(request),
    }

    return dict



def get_GET_value(request, key='', default='', blank=''):
    value = request.GET.get(key, default)
    if value == '':
        value = blank
    return value



def get_POST_value(request, key='', default='', blank=''):
     value = request.POST.get(key, default)
     if value == '':
        value = blank
     return value



def get_value(request=None, key='', default='', blank='', method=POST):
    """
        Obtiene valor de object request por los metodos POST/GET
    """
    if method == POST:
        return get_POST_value(request, key, default, blank)
    else:
        return get_GET_value(request, key, default, blank)



def time_split(cad="00:00:00"):
    """
        comvierte la cadena de texto en un objecto time
    """
    list = [int(n) for n in cad.split(":")]
    hora = datetime.time(list[0], list[1])
    return hora