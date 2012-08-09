#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
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



class ACont:
    """
        Simple Clase Contenedora para organizar informacion
    """

    def __init__(self, name='', url='', title=''):
        self.name = name
        self.url = url
        self.title = title



def user_menu(request):
    """
        carga el menu de acuerdo al tipo de usuario
    """
    if request.user.is_authenticated():
        group_name = request.user.groups.all()[0].name
        if group_name == "Pacientes":
            return load_cont(os.path.join('UsersMenu','pacientes.txt'))

        else:
            return load_cont(os.path.join('UsersMenu','admins.txt'))
    else:
        return load_cont(os.path.join('UsersMenu','not-login.txt'))



def user_info(request):
    if request.user.is_authenticated():
        return ACont(request.user.username, '/logout/', 'Cerrar Session de Usuario')
    else:
        return ACont('OFFLINE', '/login/', 'Login')



def generate_base_keys(request):
    """
        Genera el dicionario con contenido basico.
    """

    dict = {
        'user_menu': user_menu(request),
        'User': user_info(request),
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

