#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Listado de constantes q se usaran en el Sistema
"""

import os


#ruta del proyecto
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
_MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
_STATIC_ROOT = os.path.join(PROJECT_PATH, 'media/static')
MI_TEMPLATE_DIR = os.path.join(PROJECT_PATH, 'templates')

