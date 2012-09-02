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



def received(request):
    """
        Muestra todos los mensajes recividos del usuario
    """
    mi_template = get_template('GestionTurnos/inbox/mensajes-recibidos.html')
    dict = generate_base_keys(request)
    if request.user.is_authenticated():

        msjs = InboxMsj.objects.filter(to_user=request.user)
        if len(msjs) > 0:
            dict['msj_inbox'] = InboxMsj.objects.filter(to_user=request.user)
            dict['no_empty'] = True

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