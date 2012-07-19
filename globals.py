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



MONTHS = [
    'Enero',
    'Febrero',
    'Marzo',
    'Abril',
    'Mayo',
    'Junio',
    'Julio',
    'Agosto',
    'Setiembre',
    'Octubre',
    'Noviembre',
    'Diciembre'
]



#Choices varios
SEXO_CHOICE = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ('-', 'No Definido'),
)


TYPE_DOC_CHOICE = (
    ('D.N.I.', 'Documento Nacional de Identidad (Nuevo)'),
    ('DNI', 'Documento Nacional de Identidad Mercosur'),
    ('L.E.', 'Libreta de Enrrolamiento'),
    ('L.C.', 'Libreta Civica'),
    ('C.I.', 'Cedula de Identificacion'),
    ('--', 'No Definido'),
)


SOLICITUD_ESTADO_CHOICE = (
    ('P','Pendiente'),
    ('A','Aceptado'),
    ('C','Cancelado'),
)
