#!/usr/bin/env python
# -*- coding: utf-8 *-*


from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth #para login
from django.contrib.auth.models import User


from HistoriaClinica.models import *
#import GestionTurnos.forms as my_forms
from utils import *
from globals import *



def medic_show_patients_images(request, pac_id):
    """
        Muestra el listado de imagenes subidas de los diferentes examenenes
        realizados al paciente
    """
    mi_template = get_template('Medics/HistoriaClinica/mostrar-imagenes.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac'] = User.objects.get(groups__name='Paciente', username=pac_id)
        pass

    #usuario no posee permisos
    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_add_patients_images(request, pac_id):
    """
        Muestra el listado de imagenes subidas de los diferentes examenenes
        realizados al paciente
    """
    mi_template = get_template('Medics/HistoriaClinica/mostrar-imagenes.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac'] = User.objects.get(groups__name='Paciente', username=pac_id)
        pass

    #usuario no posee permisos
    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)
