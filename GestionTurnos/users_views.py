#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth #para login
from django.contrib.auth.models import User

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
        dict['user_menu'] = load_cont('not-login-menu.txt')

        dict['show_form'] = True


        #ctrl si hicieron post
        if request.method == 'POST':
            form = my_forms.RegisterForm(request.POST, auto_id=False)

            if form.is_valid():
                dict['query'] = True
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']

                #para comprobar si el usuario ya existe
                user = User.objects.filter(username=username)
                if user != None:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name =form.cleaned_data['last_name']
                    user.is_staff = False #no es admin
                    user.is_active = True #esta activo

                    UserInformation.objects.create(
                        user=user,
                        type_doc = form.cleaned_data['type_doc'],
                        nro_doc = form.cleaned_data['nro_doc'],
                        gender = form.cleaned_data['gender'],
                        phone = form.cleaned_data['phone'],
                        address = form.cleaned_data['address'],
                        matricula = 0
                    )

                else:
                    dict['form_errors'] = True
                    dict['form_e'] = 'Error: El Usuario "%s" ya se encuentra registrado' %username


                   
            else:
                dict['form'] = my_forms.RegisterForm(auto_id=False)
                dict['form_errors'] = True
                dict['form_e'] = form

        else:
            dict['form'] = my_forms.RegisterForm(auto_id=False)


    else:
        dict['user_menu'] = load_cont('paciente-menu.txt')
        pass


    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)