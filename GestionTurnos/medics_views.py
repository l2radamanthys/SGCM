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

from GestionTurnos.models import *
import GestionTurnos.forms as my_forms
from utils import *
from globals import *



def register(request):
    mi_template = get_template('GestionTurnos/medico-nuevo.html')
    dict = generate_base_keys(request)


    if request.user.has_perm('add_medic'):
        if request.method == 'POST':
            dict['form_commit'] = True

            form = my_forms.MedicRegisterForm(request.POST, auto_id=False)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']

                #para comprobar si el usuario ya existe
                try :
                    user = User.objects.get(username=username)
                    dict['exist_user'] = True
                    dict['form'] = form
                    dict['exist_user_error'] = 'Error: El Usuario "%s" ya se encuentra registrado' %username

                except User.DoesNotExist :
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name =form.cleaned_data['last_name']
                    user.is_staff = False #no es admin
                    user.is_active = True #esta activo

                    group = DjangoGroup.objects.get(name='Medicos')
                    user.groups.add(group)
                    user.save()

                    UserInformation.objects.create(
                        user=user,
                        type_doc = form.cleaned_data['type_doc'],
                        nro_doc = form.cleaned_data['nro_doc'],
                        gender = form.cleaned_data['gender'],
                        phone = form.cleaned_data['phone'],
                        address = form.cleaned_data['address'],
                        matricula = form.cleaned_data['matricula'],
                    )

                    dict['username'] = username
            else:
                dict['form_errors'] = True
                dict['form'] = my_forms.RegisterForm(auto_id=False)
                dict['form_e'] = form

        else:
            dict['form'] = my_forms.MedicRegisterForm()

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def list(request):
    """
        Lista todos los medicos
    """
    mi_template = get_template('GestionTurnos/medico-listado.html')
    dict = generate_base_keys(request)

    if request.user.has_perm('change_medic'):
        dict['modify'] = True
        dict['medics'] = User.objects.filter(groups__name='Medicos')
    else:
        dict['data'] = MedicalSpecialityFor.objects.all()


    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)




def perms_list(request):
    mi_template = get_template('GestionTurnos/perm-list.html')
    dict = generate_base_keys(request)

    #from django.contrib.auth.models import Permission

    dict['perms'] = Permission.objects.all()


    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)


def apps_list(request):
    mi_template = get_template('GestionTurnos/apps-list.html')
    dict = generate_base_keys(request)

    #from django.contrib.auth.models import Permission

    dict['apps'] = ContentType.objects.all()


    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



