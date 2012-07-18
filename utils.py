#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from globals import MI_TEMPLATE_DIR


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
