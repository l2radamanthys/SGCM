#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth #para login
from django.contrib.auth.models import User

from GestionTurnos.models import *

import HTMLTags as Tags
import my_forms
from utils import *
from globals import *



def index(request):
    """
        Pagina de inicio

        por el momento solo tiene contenido estatico que falta rellenar
    """
    mi_template = get_template('index.html')
    dict = generate_base_keys(request)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def login(request):
    """
        Vista de Inicio de session de usuarios
    """
    mi_template = get_template('login.html')
    dict = generate_base_keys(request)

    #dict['user_menu'] = load_cont('not-login-menu.txt')

    if not request.user.is_authenticated():
        dict['not_login'] = True

        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)

            if (user is not None) and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/')

            else:
                dict['login_error'] = True
    else:
        dict['username'] = request.user.username

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def logout(request):
    """
        Vista para cerrar session
    """
    mi_template = get_template('logout.html')
    dict = generate_base_keys(request)

    if request.user.is_authenticated():
        auth.logout(request)
        dict = generate_base_keys(request)
        dict['user_info'] = "Usuario no Conectado"

    else:
        dict['error'] = True


    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def restricted_access(request, area="NULL"):
    """
        Para mostrar la vista de acceso restringido
    """
    mi_template = get_template('restricted-access.html')
    dict = generate_base_keys(request)
    dict['area'] = area
    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def change_password(request):
    """
        Vista para cambiar la contraseña del usuario
    """
    if request.user.is_authenticated():
        mi_template = get_template('change-password.html')
        dict = generate_base_keys(request)

        dict['form'] = my_forms.ChangePasswordForm(auto_id=False)
        dict['show_form'] = True
        dict['show_error'] = False

        if request.method == 'POST':
            form = my_forms.ChangePasswordForm(request.POST, auto_id=False)
            if form.is_valid():

                if request.user.check_password(form.cleaned_data['old_password']):
                    #todo correcto se cambio la contrasenia
                    #user = User.ob
                    request.user.set_password(form.cleaned_data['password'])
                    request.user.save()
                    dict['show_form'] = False
                else:
                    #la contrasenia anterior no coincide
                    dict['show_error'] = True
                    dict['custom_error'] = Tags.custom_tag(content='Error Contrasenia invalida')
            else:
                dict['form'] = form
                dict['show_error'] = True

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def my_info(request):
    """
        Vista para mostrar los datos personales del usuario que
        actualmente se encuentra logueado
    """
    mi_template = get_template('mostrar-mis-datos.html')
    dict = generate_base_keys(request)

    if request.user.is_authenticated():
        #para mostrar matricula
        dict['is_medic'] = (request.user.groups.all()[0].name == "Medico")
        dict['user'] = request.user
        dict['user_data'] = UserInformation.objects.get(user__username=request.user.username)
        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def change_my_info(request):
    mi_template = get_template('modificar-mis-datos.html')
    dict = generate_base_keys(request)

    dict['show_errors'] = False
    dict['show_form'] = False
    if request.user.is_authenticated():
        if request.method == "POST" and False:
            form = my_forms.ChangeUserInformationForm(request.POST)
            if form.is_valid():
                pass
            else:
                dict['show_errors'] = True
                dict['form'] = form

        else:
            user_data = UserInformation.objects.get(user__username=request.user.username)
            form_data = {
                'type_doc': user_data.type_doc,
                'nro_doc': user_data.nro_doc,
                'gender': user_data.gender,
                'phone': user_data.phone,
                'address': user_data.address,
                'city': user_data.city,
                'state': user_data.state,
                'birth_date': user_data.birth_date,
                'matricula': user_data.matricula,
            }

            dict['form'] = my_forms.ChangeUserInformationForm(initial=form_data)
            dict['show_form'] = True


        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def change_my_avatar(request):
    mi_template = get_template('cambiar-mi-avatar.html')
    dict = generate_base_keys(request)

    if request.user.is_authenticated():
        dict['show_form'] = True
        info = UserInformation.objects.get(user=request.user)
        dict['user_data'] = info
        if request.method == "POST":
            form = my_forms.ChangeAvatarForm(request.POST, request.FILES)
            if form.is_valid():
                info.photo = form.cleaned_data['photo']
                info.save()
                return HttpResponseRedirect("/mis-datos/")
            else:
                print "Error"

        else:
            dict['form'] = my_forms.ChangeAvatarForm(auto_id=False)


        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)