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
    dict['show_form'] = True

    if request.user.is_authenticated():
        user_data = UserInformation.objects.get(user=request.user)
        form_data = {
            'type_doc': user_data.type_doc,
            'nro_doc': user_data.nro_doc,
            'gender': user_data.gender,
            'phone': user_data.phone,
            'address': user_data.address,
            'city': user_data.city,
            'state': user_data.state,
            'birth_date': user_data.birth_date.strftime("%d/%m/%Y"),
            'matricula': user_data.matricula,
        }

        _form_data = {
            'first_name' : request.user.first_name,
            'last_name' : request.user.last_name,
            'email' : request.user.email,
        }

        print user_data.birth_date.strftime("%d/%m/%Y")
        #si es medico
        if request.user.groups.all()[0].name == "Medico":
            if request.method == 'POST':
                form = my_forms.ChangeMedicInformationForm(request.POST)
                _form = my_forms.ChangeUserDataForm(request.POST)
                if form.is_valid() and _form.is_valid():
                    user = request.user
                    user.first_name = _form.cleaned_data['first_name']
                    user.last_name = _form.cleaned_data['last_name']
                    user.email = _form.cleaned_data['email']
                    user.save()

                    info = UserInformation.objects.get(user=request.user)
                    info.type_doc = form.cleaned_data['type_doc']
                    info.nro_doc = form.cleaned_data['nro_doc']
                    info.gender = form.cleaned_data['gender']
                    info.phone = form.cleaned_data['phone']
                    info.address = form.cleaned_data['address']
                    info.city = form.cleaned_data['city']
                    info.state = form.cleaned_data['state']
                    info.birth_date = form.cleaned_data['birth_date']
                    info.matricula = form.cleaned_data['matricula']
                    info.save()

                    return HttpResponseRedirect("/mis-datos/")
                else:
                    dict['show_errors'] = True
                    dict['form'] = form
                    dict['aform'] = _form
            else:
                dict['form'] = my_forms.ChangeMedicInformationForm(initial=form_data)
                dict['aform'] = my_forms.ChangeUserDataForm(initial=_form_data)

        #el resto de los usuarios
        else:
            if request.method == 'POST':
                form = my_forms.ChangeUserInformationForm(request.POST)
                _form = my_forms.ChangeUserDataForm(request.POST)
                if form.is_valid() and _form.is_valid():
                    user = request.user
                    user.first_name = _form.cleaned_data['first_name']
                    user.last_name = _form.cleaned_data['last_name']
                    user.email = _form.cleaned_data['email']
                    user.save()

                    info = UserInformation.objects.get(user=request.user)
                    info.type_doc = form.cleaned_data['type_doc']
                    info.nro_doc = form.cleaned_data['nro_doc']
                    info.gender = form.cleaned_data['gender']
                    info.phone = form.cleaned_data['phone']
                    info.address = form.cleaned_data['address']
                    info.city = form.cleaned_data['city']
                    info.state = form.cleaned_data['state']
                    info.birth_date = form.cleaned_data['birth_date']
                    info.save()
                    return HttpResponseRedirect("/mis-datos/")
                else:
                    dict['show_errors'] = True
                    dict['form'] = form
                    dict['aform'] = _form
            else:
                dict['form'] = my_forms.ChangeUserInformationForm(initial=form_data)
                dict['aform'] = my_forms.ChangeUserDataForm(initial=_form_data)


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
