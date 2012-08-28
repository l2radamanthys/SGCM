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
    """
     Vista, para registrar un Medico

    Accesso:
    --------
        - Administradores (Total)
    """
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
        Lista todos los Medicos

    Accesso:
    --------
        - Administradores
            - Visualizacion Datos
            - Menu Modificacion

        - Medicos | Pacientes | Otros
            - Visualizacion Datos
    """
    mi_template = get_template('GestionTurnos/medico-listado.html')
    dict = generate_base_keys(request)

    if request.user.has_perm('change_medic'):
        dict['modify'] = True

    dict['medics'] = User.objects.filter(groups__name='Medicos')

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def show_info(request, id=None):
    """
        Muestra los Datos Basicos del Medico
    """
    mi_template = get_template('GestionTurnos/medico-datos.html')
    dict = generate_base_keys(request)

    if request.user.has_perm('change_medic'):
        dict['modify'] = True
        
    dict['sub_title'] = "Informacion del Profecional"
    dict['user'] = User.objects.get(id = int(id))
    dict['user_info'] = UserInformation.objects.get(user__id = int(id))

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def show_medic_specialities(request, id):
    mi_template = get_template('GestionTurnos/medico-especialidades.html')
    dict = generate_base_keys(request)

    if request.user.has_perm('change_medic'):
        dict['modify'] = True

    dict['sub_title'] = "Especialidades del Profesional"
    dict['user'] = User.objects.get(id = int(id))
    dict['specialities'] = MedicalSpecialityFor.objects.filter(user__id = int(id))

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def add_medic_speciality(request, id):
    """
        Agregar una Especialidad medica, al medico
    """
    mi_template = get_template('GestionTurnos/medico-especialidades-agregar.html')
    dict = generate_base_keys(request)

    if request.user.has_perm('change_medic'):
        id = int(id)
        user_ = User.objects.get(id=id)
        
        if request.method == 'POST':
            esp = MedicalSpecialties.objects.get(id=int(get_value(request, 'especialidad')))
            med_esp = MedicalSpecialityFor(
                user = user_,
                speciality = esp
            )
            med_esp.save()
            dict['med_speciality_add']  = esp
            
        dict['user'] = user_
        dict['sub_title'] = "Agregar Especialidad Medica"
        dict['especialities'] = MedicalSpecialties.objects.exclude(id__in=MedicalSpecialityFor.objects.filter(user__id=id).values('speciality__id')).order_by('name')
        dict['med_especialities'] = MedicalSpecialityFor.objects.filter(user__id=id)
        
    else: 
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)


    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def del_medic_speciality(request, id):
    """
        Quitar una especialidad asignada a un medico
    """
    mi_template = get_template('GestionTurnos/medico-especialidades-quitar.html')
    dict = generate_base_keys(request)

    if request.user.has_perm('change_medic'):
        if request.method == 'POST':
            dict['query'] = True
            try:
                med_esp = MedicalSpecialityFor.objects.get(id=id)
                dict['query_msj'] = med_esp.speciality.name
                med_esp.delete()

            except MedicalSpecialityFor.DoesNotExist:
                pass

        else:
            id = int(id)
            dict['esp_med'] = MedicalSpecialityFor.objects.get(id=id)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def add_medic_business_hours(request, id):
    """
        Agrega Horario de Atencion
    """
    pass



def show_medic_business_hours(request, id):
    """
        Muestra los horarios de Atencion del Medico
    """
    mi_template = get_template('GestionTurnos/medico-horarios-atencion.html')
    dict = generate_base_keys(request)

    id = int(id)
    user_ = User.objects.get(id=id)
    dict['user'] = user_

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)