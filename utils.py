#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import difflib

from globals import MI_TEMPLATE_DIR, POST



class CalendarDay:
    """
    Clase contenedora para mostrar los elementos de un calendario
    parametros
    @day: la fecha
    @type:
        0- No Turno
        1- Turno Disponible
        2- Sin Turno
        3- Cancelado

    """
    def __init__(self, day, _type=0, argv=None):
        self.day = day
        self.type = _type
        self.argv = argv



def load_cont(path):
    """
        Carga Contenido desde un archivo de texto
    """
    data = open(os.path.join(MI_TEMPLATE_DIR, path)).readlines()
    cont = ""
    for line in data:
        cont += line
    return cont



def get_user_menu(request):
    """
        carga el menu de acuerdo al tipo de usuario
    """
    if request.user.is_authenticated():
        group_name = request.user.groups.all()[0].name
        #usuarios
        if group_name == "Paciente":
            return load_cont(os.path.join('Menu', 'patient.html'))
        #medicos
        elif group_name == "Medico":
            return load_cont(os.path.join('Menu', 'medic.html'))
        #administradores
        else:
            return load_cont(os.path.join('Menu', 'medic.html'))
    else:
        return load_cont(os.path.join('Menu', 'not-login.html'))



def get_user_info(request, name=False):
    if request.user.is_authenticated():
        if name:
            return "%s, %s" %(request.user.last_name, request.user.first_name)
        else:
            return request.user.username
    else:
        return "Usuario no Conectado"



def get_role(request):
    if request.user.is_authenticated():
        return "(%s)" %request.user.groups.all()[0].name
    else:
        return ""



def generate_base_keys(request):
    """
        Genera el dicionario con contenido basico.
    """
    dict = {
        'user_menu': get_user_menu(request),
        'login_username': get_user_info(request),
        'login_user': get_user_info(request, True),
        'login_user_role': get_role(request),
    }
    return dict



def get_GET_value(request, key='', default='', blank=''):
    value = request.GET.get(key, default)
    if value == '':
        value = blank
    return value



def get_POST_value(request, key='', default='', blank=''):
    """
    """
    value = request.POST.get(key, default)
    if value == '':
        value = blank
    return value



def get_value(request, key='', default='', blank='', method=POST):
    """
        Obtiene valor de object request por los metodos POST/GET
    """
    if method == POST:
        return get_POST_value(request, key, default, blank)
    else:
        return get_GET_value(request, key, default, blank)



def _get_value(request, key='', default='', blank=''):
    """
        Obtiene valor de object request de la info que se envio al
        formulario
    """
    if request.method == 'POST':
        return get_POST_value(request, key, default, blank)
    else:
        return get_GET_value(request, key, default, blank)



def time_split(cad="00:00:00"):
    """
        comvierte la cadena de texto en un objecto time
    """
    lista = [int(n) for n in cad.split(":")]
    hora = datetime.time(lista[0], lista[1])
    return hora



def dia_fecha(fechaNac):
    """
    Obtiene el dia de la fecha pasada como string en formato dd-mm-aaaa

    El codigo original pertenece a Víctor R. Varela Medina (@VitocoSan) y
    fue obtenido de:
    http://vitocosan.wordpress.com/2009/01/15/ocioque-dia-de-la-semana-naciste-python/
    """

    #dia = ['Sabado', 'Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']
    dia = (6, 7, 1, 2, 3, 4, 5)
    arrayfNac=fechaNac.split('-')
    dfNac=datetime.date(int(arrayfNac[2]),int(arrayfNac[1]),int(arrayfNac[0]))
    val1=dfNac.month
    val2=dfNac.year
    if(dfNac.month == 1):
        val1=13
        val2=val2 - 1

    if(dfNac.month == 2):
        val1=14
        val2=val2-1

    val3 = ((val1+1)*3)/5;
    val4 = val2/4
    val5 = val2/100
    val6 = val2/400
    val7 = dfNac.day+(val1*2)+val3+val2+val4-val5+val6+2
    val8 = val7/7
    val0 = val7-(val8 * 7)
    return dia[val0]


def datetime_to_time(dt):
    """
        convierte unicamente las horas,minutos y segundos de un objecto datetime
        a objecto time
    """
    t = datetime.time(
        hour=dt.hour,
        minute=dt.minute,
        second=dt.second
    )
    return t


def time_to_datetime(t):
    """
        convierte un objecto time a datetime, por defecto se le asigna la
        fecha 1/1/1900
    """
    dt = datetime.datetime(
        1900,
        1,
        1,
        t.hour,
        t.minute,
        t.second
    )
    return dt


def time_to_timedelta(t):
    """
        convierte un objecto time en timedelta
    """
    td = datetime.timedelta(
        hours = t.hour,
        minutes = t.minute,
        seconds = t.second
    )
    return td


def message_diff_insert(text1, text2):
    """
    Retorna el nuevo contenido que se inserto al texto original
    """
    diff = difflib.Differ()
    result = list(diff.compare(text1, text2))

    insert = "" #contenido insertados
    line = ""
    band = False #bandera de almacenado de linea
    for c in result:
        # + indica insercion por lo que hubo o modificacion o insersion en
        #la lines por ende se almacenara la misma
        if c[0] == '+':
            band = True

        #si hay salto de linea compruebo la variable band y reseteo las mismas
        #para la siguiente linea
        if c[-1] == '\n':
            if band:
                insert += line + c[-1]
            line = ""
            band = False

        else:
            line += c[-1]
    return insert



def date_to_str(date):
    pass