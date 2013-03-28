#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template, render_to_string
from django.template import Context
from django.contrib import auth #para login
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as DjangoGroup
#from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


import urllib

from GestionTurnos.models import *
import GestionTurnos.forms as my_forms
from utils import *
from globals import *
import HTMLTags as Tags



def patient_register(request):
    """
        Vista Para Registracion de Nuevos Usuarios
    """
    mi_template = get_template('Patients/GestionTurnos/register.html')
    dict = generate_base_keys(request)

    #para registrarse por ende tiene que ser un usuario no logueado
    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = my_forms.RegisterForm(request.POST, auto_id=False)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']

                try:
                    user = User.objects.get(username=username)
                    #el usuario ya existe genero un mensaje de error
                    dict['show_errors'] = True
                    dict['show_form'] = True #mostrar form de registro
                    dict['custon_errors'] = Tags.html_message("Error el usuario %s ya existe.." %Tags.strong(username))
                    dict['form'] = form

                except User.DoesNotExist:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name =form.cleaned_data['last_name']
                    user.is_staff = False #no es admin
                    user.is_active = False #el usuario deve ser activado mediante una confirmacion que se envia al mail
                    group = DjangoGroup.objects.get(name='Paciente')
                    user.groups.add(group)
                    user.save()

                    UserInformation.objects.create(
                        user=user,
                        type_doc = form.cleaned_data['type_doc'],
                        nro_doc = form.cleaned_data['nro_doc'],
                        gender = form.cleaned_data['gender'],
                        birth_date = form.cleaned_data['birth_date'],
                        phone = form.cleaned_data['phone'],
                        address = form.cleaned_data['address'],
                        matricula = 0
                    )

                    ## generacion y envio del mail de activacion de usuario
                    subject = "Confirmacion Registro Paciente"
                    to_email = user.email
                    from_email = "registro-usuario@sgcm.com"
                    mdict ={
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        #'activaction_key': urllib.quote_plus(user.username.encode('base64')).replace('%','?'),
                        'activaction_key': user.username.encode('base64').replace('=','6'),
                        'page_url': SITE_URL,
                    }
                    #version HTML
                    html_content = render_to_string('Mail/registrar-paciente.html', mdict)
                    #version en formato texto plano
                    text_content = strip_tags(html_content)
                    #envio el mail
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    #mensaje de confirmacion de creacion de usuario
                    dict['show_form'] = False
                    dict['custon_message'] = Tags.html_message("Paciente Registrado %s Correctamente.."  %(form.cleaned_data['first_name']), type="ok")
                    dict['query'] =  "user ok"
            else:
                dict['show_form'] = True #mostrar form de registro
                dict['show_errors'] = True
                dict['form'] = form

        else:
            dict['show_form'] = True #mostrar form de registro
            dict['show_errors'] = False
            dict['form'] = my_forms.RegisterForm(auto_id=False)

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        #si hay un usuario logueado intentanto acceder sera enviado a una
        #pagina de error
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def patient_activate(request, patient_username=None, activaction_key=None):
    """
        Vista que permite activar un usuario determinado
    """
    mi_template = get_template('Patients/GestionTurnos/activar-usuario.html')
    dict = generate_base_keys(request)

    #para registrarse por ende tiene que ser un usuario no logueado
    if not request.user.is_authenticated():

        if request.method == 'POST':
            try:
                user = User.objects.get(username=get_value(request, 'username'))
                if user.is_active:
                    dict['custom_message'] = Tags.html_message('Error: El usuario %s ya fue activado' %user.username, 'error')

                else:
                    key = get_value(request, 'key')
                    key_c = user.username.encode('base64').replace('=','6')[:-1]
                    if key == key_c:
                        dict['custom_message'] = Tags.html_message('Usuario activado', 'info')
                    else:
                        dict['show_form'] = True
                        dict['username'] = patient_username
                        dict['activation_key'] = activaction_key
                        dict['custom_message'] = Tags.html_message('Error: Codigo de activacion invalido (%s) - (%s)' %(key, key_c), 'error')


            except User.DoesNotExist:
                dict['show_form'] = True
                dict['username'] = patient_username
                dict['activation_key'] = activaction_key
                dict['custom_message'] = Tags.html_message('Error Usuario Inexistente', 'error')

        else:
            dict['show_form'] = True
            dict['username'] = patient_username
            dict['activation_key'] = activaction_key


        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        #si hay un usuario logueado intentanto acceder sera enviado a una
        #pagina de error
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

