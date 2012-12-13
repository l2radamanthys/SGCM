#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth #para login
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as DjangoGroup


from GestionTurnos.models import *
import GestionTurnos.forms as my_forms
from utils import *
from globals import *



def search(request):
    """
	Vista para buscar Paciente por similitud y mostrar el listado de
	posibles resultados
    """
    mi_template = get_template('Patients/search.html')
    dict = generate_base_keys(request)

    if True: #asignar permiso correspondiente mas adelante
	#falta implementar la busqueda en si, por ahora solo listado
	dict['search_result'] = User.objects.filter(groups__name='Pacientes')
        
    #usuario no posee permisos
    else:
	path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)


    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def show_info(request, pac_id):
    """
	Muestra la informacion del paciente especificada en pac_id
    """
    mi_template = get_template('Patients/show-info.html')
    dict = generate_base_keys(request)

    if True: #asignar permiso correspondiente mas adelante

	dict['pac'] = User.objects.get(groups__name='Pacientes', username=pac_id)
	dict['pac_inf'] = UserInformation.objects.get(user__username=pac_id)
	pass
    
    else:
	path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)


    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)