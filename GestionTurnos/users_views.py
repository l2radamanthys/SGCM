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




def register(request):
    """
        Metodo para registrar un nuevo usuario
    """
    mi_template = get_template('GestionTurnos/usuario-nuevo.html')
    dict = generate_base_keys(request)

    if not request.user.is_authenticated():
        dict['not_login'] = True

        #ctrl si hicieron post
        if request.method == 'POST':
            dict['form_commit'] = True
            form = my_forms.RegisterForm(request.POST, auto_id=False)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']

                #para comprobar si el usuario ya existe
                try :
                    user = User.objects.get(username=username)
                    
                except User.DoesNotExist :
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name =form.cleaned_data['last_name']
                    user.is_staff = False #no es admin
                    user.is_active = True #esta activo

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

                    dict['username'] = username

                else:
                    dict['exist_user'] = True
                    dict['form'] = form
                    dict['exist_user_error'] = 'Error: El Usuario "%s" ya se encuentra registrado' %username
                 
            else:
                dict['form_errors'] = True
                dict['form'] = my_forms.RegisterForm(auto_id=False)
                dict['form_e'] = form
                
        else:
            dict['form'] = my_forms.RegisterForm(auto_id=False)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def my_info(request):
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



def calendar(request,month=None, year=None):
    """
    """

    mi_template = get_template('GestionTurnos/calendar.html')
    dict = generate_base_keys(request)

    import calendar
    import datetime

    

    if month != None and year != None:
        month = int(month) % 13
        year = int(year)

    else:
        year = datetime.date.today().year
        month = datetime.date.today().month

    #hoy
    t_year = datetime.date.today().year
    t_month = datetime.date.today().month

    cal = calendar.Calendar()
    wekends = cal.monthdayscalendar(year, month)

    dict['month'] = MONTHS[month-1]
    dict['year'] = year
    dict['wekends'] = wekends

    if month == 1:
        dict['prev_month'] = 12
        dict['next_month'] = 2
        dict['prev_year'] = year - 1
        dict['next_year'] = year

    elif month == 12:
        dict['prev_month'] = 11
        dict['next_month'] = 1
        dict['prev_year'] = year
        dict['next_year'] = year + 1
    
    else:
        dict['prev_month'] = month - 1
        dict['next_month'] = month + 1
        dict['prev_year'] = year
        dict['next_year'] = year

    if dict['prev_month'] < t_month and dict['prev_year'] == t_year or dict['prev_year'] < t_year:
        dict['prev_month'] = t_month
        dict['prev_year'] = t_year


    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)