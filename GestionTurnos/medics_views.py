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

import calendar
import datetime

from GestionTurnos.models import *
import GestionTurnos.forms as my_forms
from utils import *
from globals import *
import HTMLTags as Tags


def patients_search(request):
    """
    Vista para buscar Paciente por similitud y mostrar el listado de
    posibles resultados
    """
    mi_template = get_template('Medics/GestionTurnos/patients-search.html')
    dict = generate_base_keys(request)

    if True: #asignar permiso correspondiente mas adelante
        #busqueda de pacientes
        field = get_value(request, 'field')
        argv = get_value(request, 'search')

        if field == 'u':
            dict['search_result'] = User.objects.filter(groups__name='Paciente', username__contains=argv)
        elif field == 'n':
            dict['search_result'] = User.objects.filter(groups__name='Paciente', first_name__contains=argv)
        elif field == 'a':
            dict['search_result'] = User.objects.filter(groups__name='Paciente', last_name__contains=argv)
        else:
            dict['search_result'] = User.objects.filter(groups__name='Paciente')

    #usuario no posee permisos
    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def patient_show_info(request, pac_id):
    """
    Muestra la informacion del paciente especificada en pac_id
    """
    mi_template = get_template('Medics/GestionTurnos/patients-show-info.html')
    dict = generate_base_keys(request)
    dict['pac_username'] = pac_id

    if True: #asignar permiso correspondiente mas adelante
        dict['pac'] = User.objects.get(groups__name='Paciente', username=pac_id)
        dict['pac_inf'] = UserInformation.objects.get(user__username=pac_id)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def patient_edit_basic_info(request, pac_id):
    """
    Vista para la modificacion de los datos basicos del Paciente
    """
    mi_template = get_template('Medics/GestionTurnos/patient-edit-basic-info.html')
    dict = generate_base_keys(request)

    if True: #asignar permiso correspondiente mas adelante
        pac = User.objects.get(groups__name='Paciente', username=pac_id)
        pac_inf = UserInformation.objects.get(user=pac)
        dict['pac_inf'] = pac_inf

        if request.method == 'POST':
            dict['show_form'] = False
            dict['custon_message'] = "Form enviado"
            form = my_forms.BasicInfoForm(request.POST, request.FILES)
            if form.is_valid():
                pac.first_name = form.cleaned_data['first_name']
                pac.last_name = form.cleaned_data['last_name']
                pac_inf.type_doc = form.cleaned_data['type_doc']
                pac_inf.nro_doc = form.cleaned_data['nro_doc']
                pac_inf.gender = form.cleaned_data['gender']
                pac_inf.address = form.cleaned_data['address']
                pac_inf.city = form.cleaned_data['city']
                pac_inf.state = form.cleaned_data['state']
                pac_inf.phone = form.cleaned_data['phone']
                pac_inf.photo = form.cleaned_data['photo']
                pac.save()
                pac_inf.save()
                dict['update_ok'] = True
                dict['pac_username'] = pac.username

            else:
                 dict['custon_message'] = "Error"
                 dict['show_errors'] = True
                 dict['form'] = form = my_forms.BasicInfoForm(request.POST)

        else:
            dict['show_form'] = True
            dict['pac_username'] = pac.username

            form_data = { #contenido precargado que tendra el formulario
                'email' : pac.email,
                'first_name' : pac.first_name,
                'last_name' : pac.last_name,
                'type_doc' : pac_inf.type_doc,
                'nro_doc' : pac_inf.nro_doc,
                'gender' : pac_inf.gender,
                'city' : pac_inf.city,
                'state' : pac_inf.state,
                'address' : pac_inf.address,
                'phone' : pac_inf.phone,
            }
            dict['form'] = my_forms.RegisterForm(form_data, auto_id=False)

    else: #redireccionar sitio error
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def patient_show_medical_consultation(request, pac_id):
    """
    Muestra las consultas medicas de un paciente en particular
    """
    mi_template = get_template('Medics/GestionTurnos/patient-show-medical-consultation.html')
    dict = generate_base_keys(request)

    dict['pac_username'] = pac_id

    is_medic = True
    if is_medic:
        dict['pac'] = User.objects.get(groups__name='Paciente', username=pac_id)
        dict ['medicals_consultations'] = MedicalConsultation.objects.filter(patient__username=pac_id)
        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def patient_register(request):
    """
    Vista para registrar un nuevo usuario, paciente
    """
    #mi_template = get_template('Patients/GestionTurnos/register.html')
    mi_template = get_template('Medics/GestionTurnos/registrar-paciente.html')
    dict = generate_base_keys(request)

    is_medic = True
    if is_medic:
        dict['show_form'] = True
        dict['user_type'] = "Paciente"
        dict['show_errors'] = False
        dict['form'] = my_forms.RegisterForm(auto_id=False)

        if request.method == 'POST':
            dict['query'] = "POST"  #debug only
            form = my_forms.RegisterForm(request.POST, request.FILES, auto_id=False)
            if form.is_valid():
                dict['query'] += " | FORM OK"  #debug only
                _username = form.cleaned_data['username']
                _password = form.cleaned_data['password']
                _email = form.cleaned_data['email']

                #comprobacion si el usuario ya existe
                try:
                    # error el nombre de usuario existe
                    user = User.objects.get(username=_username)
                    dict['show_errors'] = True
                    dict['custon_errors'] = Tags.html_message("Error el usuario %s ya existe.." %Tags.strong(_username))
                    dict['form'] = form
                    dict['query'] += " | USER ERROR"  #debug only

                except User.DoesNotExist:
                    user = User.objects.create_user(username=_username, email=_email, password=_password)
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name =form.cleaned_data['last_name']
                    user.is_staff = False #no es admin
                    user.is_active = True #esta activo despues cambio, para hacer algun modo de activacion
                    user.save()

                    group = DjangoGroup.objects.get(name='Paciente')
                    user.groups.add(group)

                    UserInformation.objects.create(
                            user=user,
                            type_doc = form.cleaned_data['type_doc'],
                            nro_doc = form.cleaned_data['nro_doc'],
                            gender = form.cleaned_data['gender'],
                            phone = form.cleaned_data['phone'],
                            address = form.cleaned_data['address'],
                            birth_date = form.cleaned_data['birth_date'],
                            city = form.cleaned_data['city'],
                            state = form.cleaned_data['state'],
                            photo = form.cleaned_data["photo"], #causa error que no pude resolver cuando intento agregar foto al crearlo
                            matricula = "No Medic"
                    )
                    dict['show_form'] = False
                    dict['custon_message'] = Tags.html_message("Paciente <strong>%s</strong> Registrado Correctamente.."  %(form.cleaned_data['first_name']+form.cleaned_data['last_name']), type="ok")

            else:
                dict['query'] += " | FORM ERROR"  #debug only
                dict['show_errors'] = True
                dict['form_errors'] = True
                dict['form'] = form

        else: #si no se envio el formulario
            dict['query'] = "NO COMMIT"  #debug only
            dict['form'] = my_forms.RegisterForm(auto_id=False)
            dict['label']= "aaa"

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else: #sale por aca si el usuario no tiene permiso
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def medic_register(request):
    """
     Vista, para registrar un Paciente

    Accesso:
    --------
        - Administradores (Total)
    - Medicos
    """
    mi_template = get_template('GestionTurnos/medico-nuevo.html')
    dict = generate_base_keys(request)

    if is_admin:
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

                    dict['name'] = user.get_full_name()
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



# vistas remannetes de  la version anterior no se implementaron de nuevo por lo que nos las
# agrego

#def medics_list(request):
    #"""
    #
    #"""
    #mi_template = get_template('GestionTurnos/medico-listado.html')
    #dict = generate_base_keys(request)

    #if request.user.has_perm('change_medic'):
        #dict['modify'] = True

    #dict['medics'] = User.objects.filter(groups__name='Medicos')

    #html_cont = mi_template.render(Context(dict))
    #return HttpResponse(html_cont)


#def medic_show_specialities(request, id):
    #mi_template = get_template('GestionTurnos/medico-especialidades.html')
    #dict = generate_base_keys(request)

    #if request.user.has_perm('change_medic'):
        #dict['modify'] = True

    #dict['sub_title'] = "Especialidades del Profesional"
    #dict['user'] = User.objects.get(id = int(id))
    #dict['specialities'] = MedicalSpecialityFor.objects.filter(user__id = int(id))

    #html_cont = mi_template.render(Context(dict))
    #return HttpResponse(html_cont)



#def medic_add_speciality(request, id):
    #"""
        #Agregar una Especialidad medica, al medico
    #"""
    #mi_template = get_template('GestionTurnos/medico-especialidades-agregar.html')
    #dict = generate_base_keys(request)

    #if request.user.has_perm('change_medic'):
        #id = int(id)
        #user_ = User.objects.get(id=id)

        #if request.method == 'POST':
            #esp = MedicalSpecialties.objects.get(id=int(get_value(request, 'especialidad')))
            #med_esp = MedicalSpecialityFor(
                #user = user_,
                #speciality = esp
            #)
            #med_esp.save()
            #dict['med_speciality_add']  = esp

        #dict['user'] = user_
        #dict['sub_title'] = "Agregar Especialidad Medica"
        #dict['especialities'] = MedicalSpecialties.objects.exclude(id__in=MedicalSpecialityFor.objects.filter(user__id=id).values('speciality__id')).order_by('name')
        #dict['med_especialities'] = MedicalSpecialityFor.objects.filter(user__id=id)

    #else:
        #path = request.META['PATH_INFO']
        #return HttpResponseRedirect("/restricted-access%s" %path)

    #html_cont = mi_template.render(Context(dict))
    #return HttpResponse(html_cont)



#def del_medic_speciality(request, id):
    #"""
        #Quitar una especialidad asignada a un medico
    #"""
    #mi_template = get_template('GestionTurnos/medico-especialidades-quitar.html')
    #dict = generate_base_keys(request)

    #if request.user.has_perm('change_medic'):
        #if request.method == 'POST':
            #dict['query'] = True
            #try:
                #med_esp = MedicalSpecialityFor.objects.get(id=id)
                #dict['query_msj'] = med_esp.speciality.name
                #med_esp.delete()

            #except MedicalSpecialityFor.DoesNotExist:
                #pass

        #else:
            #id = int(id)
            #dict['esp_med'] = MedicalSpecialityFor.objects.get(id=id)

    #else:
        #path = request.META['PATH_INFO']
        #return HttpResponseRedirect("/restricted-access%s" %path)

    #html_cont = mi_template.render(Context(dict))
    #return HttpResponse(html_cont)



def my_medic_show_business_hours(request):
    """
        Muestra mis dias y horario de atencion
    """

    if True: #por ahora no controlo permisos
        mi_template = get_template('Medics/GestionTurnos/mis-horarios-atencion.html')
        dict = generate_base_keys(request)
        dict['business_hours'] = BusinessHours.objects.filter(user__username=request.user.username)

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def my_medic_add_business_hours(request):
    """
    Agregar un Horario Atencion a mi usuario Medico
    """
    if True: #por ahora no controlo permisos
        mi_template = get_template('Medics/GestionTurnos/nuevo-horario-atencion.html')
        dict = generate_base_keys(request)
        dict['show_form'] = True
        if request.method == 'POST':
            form = my_forms.BusinessHoursForm(request.POST, auto_id=False)
            if form.is_valid():
                _date = int(form.cleaned_data['date'])
                query = BusinessHours.objects.filter(user=request.user, date=_date)
                if len(query) == 0:
                    dict['show_form'] = False
                    business_hour = BusinessHours(
                            user = request.user,
                            date = _date,
                            start_time = time_split(form.cleaned_data['start_time']), #
                            #start_time = time_split(_get_value(request, 'start_time')),
                            end_time = time_split(form.cleaned_data['end_time']),
                            turn_duration = int(form.cleaned_data['turn_duration']),
                    )
                    business_hour.save()
                    return HttpResponseRedirect("/medicos/mostrar/mis-horarios-atencion/")

                else:
                    dict['form'] = form
                    dict['show_errors'] = True
                    dict['custon_errors'] = '<p>Error: El dia <strong> %s </strong> ya posee un horario de atencion Asignado</p>' %DAYS[_date-1]

            else:
                dict['form'] = form
                dict['show_errors'] = True

        else:
            dict['form'] = my_forms.BusinessHoursForm(auto_id=False)


        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def my_medic_del_business_hours(request, bh_id):
    """
        Elimina un horario de atencion del medico
    """
    if True: #por ahora no controlo permisos
        mi_template = get_template('Medics/GestionTurnos/borrar-horario-atencion.html')
        dict = generate_base_keys(request)

        bh = BusinessHours.objects.get(id=int(bh_id))
        if request.method == 'POST':
            dict['query'] = True
            bh.delete()

        else:
            dict['bh_date'] = DAYS[bh.date-1]
            dict['bh_inicio'] = bh.start_time
            dict['bh_fin'] = bh.end_time
            dict['bh_duracion'] = bh.turn_duration

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



#def medic_show_business_hours(request, id):
    #"""
        #Muestra los horarios de Atencion de un medico en particular
    #"""
    #mi_template = get_template('GestionTurnos/Medics/medico-horarios-atencion.html')
    #dict = generate_base_keys(request)

    #id = int(id)
    #user_ = User.objects.get(id=id)
    #dict['user'] = user_
    #dict['business_hours'] = BusinessHours.objects.filter(user=user_)

    #if request.user.has_perm('change_medic'):
        #dict['modify'] = True

    #html_cont = mi_template.render(Context(dict))
    #return HttpResponse(html_cont)


#def medic_add_business_hours(request, id):
    #"""
        #Agrega un Horario de Atencion a la Agenda del Medico

    #Accesso:
    #--------
        #- Administradores
    #"""
    #mi_template = get_template('GestionTurnos/medico-horarios-atencion-nuevo.html')
    #dict = generate_base_keys(request)

    #user_ = User.objects.get(id=id)
    #dict['user'] = user_

    #if request.user.has_perm('change_medic'):
        #if request.method == 'POST':
            #dict['query'] = True
            #form = my_forms.BusinessHoursForm(request.POST, auto_id=False)
            #if form.is_valid():
                #business_hour = BusinessHours(
                    #user = user_,
                    #date = form.cleaned_data['date'],
                    #start_time = time_split(form.cleaned_data['start_time']),
                    #end_time = time_split(form.cleaned_data['end_time']),
                    #turn_duration = int(form.cleaned_data['turn_duration']),
                #)
                #business_hour.save()

            #else:
                #dict['form_error'] = form
        #dict['form'] = my_forms.BusinessHoursForm()
        #dict['business_hours'] = BusinessHours.objects.filter(user=user_)

    #else:
        #path = request.META['PATH_INFO']
        #return HttpResponseRedirect("/restricted-access%s" %path)

    #html_cont = mi_template.render(Context(dict))
    #return HttpResponse(html_cont)



def my_medic_show_nonworking_days(request, month=None, year=None):
    """
    """
    mi_template = get_template('Medics/GestionTurnos/dias-no-laborales.html')
    dict = generate_base_keys(request)

    if True:
        if month != None and year != None:
            month = int(month) % 13
            year = int(year)

        else:
            year = datetime.date.today().year
            month = datetime.date.today().month

        #hoy
        t_year = datetime.date.today().year
        t_month = datetime.date.today().month

        dict['month'] = month
        dict['name_month'] = MONTHS[month-1]
        dict['year'] = year

        cal = calendar.Calendar()
        wekends = cal.monthdayscalendar(year, month)

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
            dict['prev_year'] = year - 1
            dict['next_year'] = year + 1

        if dict['prev_month'] < t_month and dict['prev_year'] == t_year or dict['prev_year'] < t_year:
            dict['prev_month'] = t_month
            dict['prev_year'] = t_year


        #dias que se atiende
        bh = BusinessHours.objects.filter(user=request.user)
        wd = []
        for day in bh:
            wd.append(day.date - 1)

        #dias no laborales
        nwd = NonWorkingDay.objects.filter(user=request.user, date__month=month, date__year=year)
        _nwd = []
        for obj in nwd:
            _nwd.append(obj.date.day)

        #dias con turnos asignados
        _dta = []
        dof = DayOfAttention.objects.filter(business_hour__user=request.user, date__month=month, date__year=year)
        for day in dof:
            if day.number_of_turns > 0:
                _dta.append(day.date - 1)


        #formateo del mes
        semanas = []
        for week in wekends:
            sem = []
            i = 0
            for day in week:
                if day in _nwd: #es un dia no laboral?
                    sem.append(CalendarDay(day,2))
                else:
                    if i in wd:#dias donde se atiende
                        if day in _dta:
                            sem.append(CalendarDay(day,3)) #hay turnos asignados no se puede cancelar
                        else:
                            sem.append(CalendarDay(day,1)) #hay turnos libres
                    else:
                        sem.append(CalendarDay(day,0)) #dias q no se atiende
                i += 1
            semanas.append(sem)
        dict['wekends'] = semanas

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)





def my_medic_add_nonworking_day(request, day, month, year):
    """
    """
    mi_template = get_template('Medics/GestionTurnos/agregar-dia-no-laboral.html')
    dict = generate_base_keys(request)

    if True:
        if request.method == 'POST':
            nwd = NonWorkingDay(
            date = datetime.date(int(year), int(month), int(day)),
            issue = get_value(request, 'issue'),
            user = request.user
            )
            nwd.save()
            return HttpResponseRedirect("/medicos/mostrar/dias-no-laborales/%s/%s/" %(month, year))

        else:
            dict['show_form'] = True
            dict['day'] = day
            dict['month'] = month
            dict['year'] = year

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def my_medic_del_nonworking_day(request, day, month, year):
    """
        Vista para eliminar un dia de Atencion
    """
    mi_template = get_template('Medics/GestionTurnos/cancelar-dia-no-laboral.html')
    dict = generate_base_keys(request)

    if True:
        pass

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def my_add_medical_consultation(request, pac_id):
    """
    Agregar consulta Medica de un paciente
    """
    mi_template = get_template('Medics/GestionTurnos/agregar-consulta-medica.html')
    dict = generate_base_keys(request)

    if True:
        pac = User.objects.get(username=pac_id)
        if request.method == 'POST':
            cm = MedicalConsultation(
                    medic = request.user,
                    patient = pac,
                    issue = get_value(request, 'issue'),
                    diagnostic = get_value(request, 'diagnostic'),
                    physical_exam = get_value(request, 'physical_exam'),
                    observations = get_value(request, 'observations')
            )
            cm.save()
            dict['pac'] = pac

        else:
            dict['show_form'] = True
            dict['med'] = request.user
            dict['pac'] = pac

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def my_edit_medical_consultation(request, cm_id):
    """
        Modifica la informacion de los datos de una consulta medica
    """
    mi_template = get_template('Medics/GestionTurnos/modificar-consulta-medica.html')
    dict = generate_base_keys(request)

    if True:
        cm = MedicalConsultation.objects.get(id=cm_id)
        dict['cm'] = cm
        if request.method == 'POST':
            cm.issue = get_value(request, 'issue')
            cm.diagnostic = get_value(request, 'diagnostic')
            cm.physical_exam = get_value(request, 'physical_exam')
            cm.observations = get_value(request, 'observations')
            cm.save()
            dict['custon_messages'] = Tags.html_message('Cambios Guardados..', 'success')

        else:
            dict['med'] = cm.medic
            dict['pac'] = cm.patient

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def my_show_medical_consultation(request, cm_id):
    """
        Muestra informacion de los datos de una consulta medica
    """
    mi_template = get_template('Medics/GestionTurnos/mostrar-consulta-medica.html')
    dict = generate_base_keys(request)

    if True:
        cm = MedicalConsultation.objects.get(id=cm_id)
        dict['cm'] = cm
        if request.method == 'POST':
            cm.issue = get_value(request, 'issue')
            cm.diagnostic = get_value(request, 'diagnostic')
            cm.physical_exam = get_value(request, 'physical_exam')
            cm.observations = get_value(request, 'observations')
            cm.save()
            dict['custon_messages'] = Tags.html_message('Cambios Guardados..', 'success')

        else:
            dict['med'] = cm.medic
            dict['pac'] = cm.patient

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def my_delete_medical_consultation(request, cm_id):
    """
        Eliminar una consulta medica
    """
    mi_template = get_template('Medics/GestionTurnos/borrar-consulta-medica.html')
    dict = generate_base_keys(request)

    if True: #requiere permiso del medico
        cm = MedicalConsultation.objects.get(id=cm_id)
        if request.method == 'POST':
            cm.delete()

            return HttpResponseRedirect("/pacientes/mostrar/consultas-medicas/%s/" %cm.patient.username)

        else:
            dict['cm'] = cm
            html_cont = mi_template.render(Context(dict))
            return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def show_cronogram(request):
    """
    Muestra el cronograma los mensajes Pendientes Para el Dia y Demas.
    """
    mi_template = get_template('Medics/GestionTurnos/mostrar-cronograma.html')
    dict = generate_base_keys(request)

    if True: #requiere permiso del medico

        #fecha a controlar
        _date = datetime.date.today()
        dict['date'] = _date
        medic = request.user
        #mensajes no leidos
        messages = Message.objects.filter(read=False, to_user=request.user)
        if len(messages) > 0:
            dict['have_msj'] = True
            dict['num_msj'] = len(messages)

        #turnos para el dia
        turns = Turn.objects.filter(day__date=_date, medic=request.user)
        if len(turns) == 0:
            dict['not_turns'] = True
        dict['turns'] = turns

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def show_turns(request, day=None, month=None, year=None):
    """
        Muestra los
    """
    mi_template = get_template('Medics/GestionTurnos/mostrar-turnos-dia.html')
    dict = generate_base_keys(request)

    if True: #requiere permiso del medico

        #si no se pasa la fecha se toma el dia actual
        if day == None:
            date = datetime.datetime.today()
            day = date.day
            month = date.month
            year = date.year

        #fecha a controlar
        _date = datetime.date(int(year), int(month), int(day))
        turns = Turn.objects.filter(day__date=_date, medic=request.user)
        dict['date'] = _date
        if len(turns) == 0:
            dict['not_turns'] = True
        dict['turns'] = turns

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def select_date_to_show_turns(request, month=None, year=None):
    """
        Seleciona Dia Para Mostrar Turnoss
    """

    if True: #requiere permiso del medico
        mi_template = get_template('Medics/GestionTurnos/selecionar-dia-mostrar-turnos.html')
        dict = generate_base_keys(request)

        if month != None and year != None:
            month = int(month) % 13
            year = int(year)

        else:
            date = datetime.date.today()
            month = date.month
            year = date.year

        dict['month'] = month
        dict['name_month'] = MONTHS[month-1]
        dict['year'] = year

        cal = calendar.Calendar()
        wekends = cal.monthdayscalendar(year, month)

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

        dict['y_prev_year'] = year - 1
        dict['y_next_year'] = year + 1


        #dias que se atiende
        bh = BusinessHours.objects.filter(user=request.user)
        wd = []
        for day in bh:
            wd.append(day.date - 1)

        #dias no laborales
        nwd = NonWorkingDay.objects.filter(user=request.user, date__month=month, date__year=year)
        _nwd = []
        for obj in nwd:
            _nwd.append(obj.date.day)

        #dias con turnos asignados
        _dta = []
        dof = DayOfAttention.objects.filter(business_hour__user=request.user, date__month=month, date__year=year)
        for day in dof:
            if day.number_of_turns > 0:
                _dta.append(day.date.day - 1)


        #formateo del mes
        semanas = []
        for week in wekends:
            sem = []
            i = 0
            for day in week:
                if day in _nwd: #es un dia no laboral?
                    sem.append(CalendarDay(day,2))
                else:
                    if i in wd:#dias donde se atiende
                        if day in _dta:
                            sem.append(CalendarDay(day,3)) #hay turnos asignados no se puede cancelar
                        else:
                            sem.append(CalendarDay(day,1)) #hay turnos libres
                    else:
                        sem.append(CalendarDay(day,0)) #dias q no se atiende
                i += 1
            semanas.append(sem)
        dict['wekends'] = semanas


        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)
