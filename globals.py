#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Listado de constantes globales que se usaran en el Sistema
"""

import os


#ruta del proyecto
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
#archivos estatiticos
_MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
_STATIC_ROOT = os.path.join(PROJECT_PATH, 'media/static')
#path del directorio de plantillas
MI_TEMPLATE_DIR = os.path.join(PROJECT_PATH, 'templates')

#url del sitio web
SITE_URL = '127.0.0.1'



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

DAYS = [
    'Lunes',
    'Martes',
    'Miercoles',
    'Jueves',
    'Viernes',
    'Sabado',
    'Domingo'
]


GET = 0
POST = 1


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
    ('--', 'Otro'),
)


SOLICITUD_ESTADO_CHOICE = (
    ('P', 'Pendiente'),
    ('A', 'Aceptado'),
    ('C', 'Cancelado'),
)


TURN_STATUS_CHOICE = (
    (0, 'Pendiente'),
    (1, 'Concretada'),
    (2, 'Cancelado Medico'),
    (3, 'Cancelado Paciente'),
    (4, 'Vencido'),
)


DATE_CHOICE = (
    (1, 'Lunes'),
    (2, 'Martes'),
    (3, 'Miercoles'),
    (4, 'Jueves'),
    (5, 'Viernes'),
    (6, 'Sabado'),
    (7, 'Domingo'),
)


DAY_OF_ATTENTION_STATUS_CHOICE = (
    (0, 'Vacio'),
    (1, 'Disponible'),
    (2, 'Completo'),
)


ARG_STATES_CHOICE = (
    ("Buenos Aires", "Buenos Aires"),
    ("Catamarca", "Catamarca"),
    ("Chaco", "Chaco"),
    ("Chubut", "Chubut"),
    ("C.A.B.A.", "C.A.B.A."),
    ("Córdoba", "Córdoba"),
    ("Corrientes", "Corrientes"),
    ("Entre Ríos", "Entre Ríos"),
    ("Formosa", "Formosa"),
    ("Jujuy", "Jujuy"),
    ("La Pampa", "La Pampa"),
    ("La Rioja", "La Rioja"),
    ("Mendoza", "Mendoza"),
    ("Misiones", "Misiones"),
    ("Neuquén", "Neuquén"),
    ("Río Negro", "Río Negro"),
    ("Salta", "Salta"),
    ("San Juan", "San Juan"),
    ("San Luis", "San Luis"),
    ("Santa Cruz", "Santa Cruz"),
    ("Santa Fe", "Santa Fe"),
    ("Santiago del Estero", "Santiago del Estero"),
    ("Tierra del Fuego", "Tierra del Fuego"),
    ("Tucumán", "Tucumán"),
)

TRUE_FALSE_CHOICE = (
    ('S', 'Si'),
    ('N', 'No'),
    ('-', '--'),
)
