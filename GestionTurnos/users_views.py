#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth #para login
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as DjangoGroup

import calendar
import datetime

from GestionTurnos.models import *
import GestionTurnos.forms as my_forms
from utils import *
from globals import *
import HTMLTags as Tags



def register(request):
    """
    Vista para registrar un nuevo usuario, paciente
    """
    mi_template = get_template('Patients/register.html')
    dict = generate_base_keys(request)

    is_medic = True
    if not request.user.is_authenticated() or is_medic:
	dict['show_form'] = True
	dict['show_errors'] = False
	dict['form'] = my_forms.RegisterForm(auto_id=False)

	if request.method == 'POST':
	    form = my_forms.RegisterForm(request.POST, auto_id=False)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']

		#comprobacion si el usuario ya existe
                try :
                    user = User.objects.get(username=username)
		    # error el nombre de usuario existe
		    dict['show_errors'] = True 
		    dict['custon_errors'] = Tags.html_message("Error el usuario %s ya existe.." %Tags.strong(username))
		    dict['form'] = form

                except User.DoesNotExist :
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name =form.cleaned_data['last_name']
                    user.is_staff = False #no es admin
                    user.is_active = True #esta activo despues cambio, para hacer algun modo de activacion
		    user.save()

                    group = DjangoGroup.objects.get(name='Pacientes')
                    user.groups.add(group)

                    UserInformation.objects.create(
                        user=user,
                        type_doc = form.cleaned_data['type_doc'],
                        nro_doc = form.cleaned_data['nro_doc'],
                        gender = form.cleaned_data['gender'],
                        phone = form.cleaned_data['phone'],
                        address = form.cleaned_data['address'],
                        matricula = 0
                    )
		    dict['show_form'] = False
		    dict['custon_message'] = Tags.html_message("Paciente Registrado %s Correctamente.."  %(form.cleaned_data['first_name']), type="ok")

	    else:
		dict['show_errors'] = True
		dict['form'] = form

	else: #si no se envio el formulario
	    dict['form'] = my_forms.RegisterForm(auto_id=False)

    else: #sale por aca si el usuario no tiene permiso
	pass

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def show_my_info(request):
    """
        muestra la informacion del usuario actual que se encuentra logueado
    """
    mi_template = get_template('GestionTurnos/usuario-datos.html')
    dict = generate_base_keys(request)

    if request.user.is_authenticated():
        dict['sub_title'] = "Mis Datos"
        dict['user'] = request.user
        dict['user_info'] = UserInformation.objects.get(user__id = request.user.id)
        pass
    
    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)







