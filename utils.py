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

        if self.name == "":
            name = "OFFLINE"
            self.url = ""
            self.title = ""


def generate_base_keys(request):
    """
        Genera el dicionario con contenido basico.
    """

    dict = {
        'javascript': '',
        'style': '',
        'user_info': ACont(request.user.username, '/logout/', 'Cerrar Session de Usuario'),
    }
    
    
    
    return dict
