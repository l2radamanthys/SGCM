#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth #para login
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as DjangoGroup

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from utils import *
from globals import *
from GestionTurnos.models import *
from GestionTurnos.forms import MessageSendForm


def send_message(request):
    """
        Vista Para enviar un Mensaje
    """
    mi_template = get_template('Messages/redactar.html')
    dict = generate_base_keys(request)

    if True: #solo los medicos y administradores podran acceder a esta vista
        dict['show_form'] = True
        if request.method == 'POST':
            form = MessageSendForm(request.POST, auto_id=False)
            if form.is_valid():
                to_username = form.cleaned_data['to_user']
                try:
                    _to_user = User.objects.get(username=to_username)
                    #usuario existe y se registra el envio del mensaje
                    Message.objects.create(
                        from_user = request.user,
                        to_user = _to_user,
                        issue = form.cleaned_data['issue'],
                        content = form.cleaned_data['content'],
                    )
                    dict['show_form'] = False

                except User.DoesNotExist:
                    #el usuario destinatario no existe por lo que lanzo una exepcion
                    #personalizada que en realidad es un mensaje de error
                    dict['custom_error'] = Tags.custom_tag(content='Error Destinatario inexistente..!')
                    dict['show_error'] = True
                    dict['form'] = form

            else:
                dict['show_error'] = True
                dict['form'] = form
        else:
            dict['form'] = MessageSendForm(auto_id=False)


    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def received(request):
    """
        Muestra todos los mensajes recividos del usuario
    """
    mi_template = get_template('Messages/recibidos.html')
    dict = generate_base_keys(request)
    if request.user.is_authenticated():
        messages = Message.objects.filter(to_user=request.user)
        if len(messages) > 0:
            dict['messages'] = messages
            dict['not_empty'] = True


    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def read(request, msj_id):
    """
        Muestra un Mensaje en Particular
    """
    mi_template = get_template('GestionTurnos/inbox/mensajes-mostrar.html')
    dict = generate_base_keys(request)
    if request.user.is_authenticated():
        dict['message'] = InboxMsj.objects.filter(to_user=request.user).get(id=int(msj_id))


    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)
