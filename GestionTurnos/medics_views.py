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

import calendar, datetime

from GestionTurnos.models import *
import GestionTurnos.forms as my_forms
from utils import *
from globals import *
import HTMLTags as Tags
import reports



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
                    dict['custon_message'] = Tags.html_message("Paciente <strong>%s</strong> Registrado Correctamente.."  %(user.first_name + ' ' + user.last_name), type="success")

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



def my_medic_edit_business_hours(request, bh_id):
    """
        Modificar Horario de Atencion del Medico
    """
    if have_acess(request, ['Medico']):
        mi_template = get_template('Medics/GestionTurnos/modificar-horario-atencion.html')
        dict = generate_base_keys(request)
        dict['show_form'] = True
        dict['show_errors'] = False
        bh = BusinessHours.objects.get(id=bh_id)
        
        if request.method == 'POST':
            form = my_forms.BusinessHoursForm(request.POST)
            if form.is_valid():
                bh.date = form.cleaned_data['date']
                bh.start_time = form.cleaned_data['start_time']
                bh.end_time = form.cleaned_data['end_time']
                bh.turn_duration = form.cleaned_data['turn_duration']
                bh.save()
                
                return HttpResponseRedirect("/medicos/mostrar/mis-horarios-atencion/")
            else:
                dict['show_errors'] = True
                dict['form'] = form

        else:
            form_data = {
                    'date': bh.date,
                    'start_time': bh.start_time,
                    'end_time': bh.end_time,
                    'turn_duration': bh.turn_duration
            }
            form = my_forms.BusinessHoursForm(form_data)
            dict['form'] = form

          

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
                _dta.append(day.date - datetime.timedelta(1))

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

    if have_acess(request, ['Medico']):
        medic = request.user
        
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
        dict['precriptions'] = MedicalPrescription.objects.filter(med_consulation=cm)

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
        Muestra los turnos solicitados al medico en una fecha en particular
    """
    mi_template = get_template('Medics/GestionTurnos/mostrar-turnos-dia.html')
    dict = generate_base_keys(request)

    if have_acess(request, ['medic']): #requiere permiso del medico
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
            #dict['not_turns'] = True
            pass
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
    if have_acess(request): #requiere permiso del medico
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



## Recetas Medicas
def medic_list_patient_prescriptions(request, patient):
    """
        Listado Prescripciones Medicas
    """
    mi_template = get_template('Medics/GestionTurnos/listado-receta-medica.html')
    dict = generate_base_keys(request)

    if have_acess(request):
        dict['pac_username'] = patient
        pac = User.objects.get(groups__name='Paciente', username=patient)
        dict['pac'] = pac

        dict['prescs_medics'] = MedicalPrescription.objects.filter(med_consulation__patient = pac)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_add_patient_prescription(request, id_pm):
    """
        Agregar receta medica
    """
    mi_template = get_template('Medics/GestionTurnos/agregar-receta-medica.html')
    dict = generate_base_keys(request)

    if have_acess():
        mc = MedicalConsultation.objects.get(id=id_pm)
        dict['mc'] = mc
        dict['pac'] = mc.patient
        dict['show_form'] = True
        dict['show_errors'] = False

        if request.method == "POST":
            form = my_forms.MedicalPrescriptionForm(request.POST)
            if form.is_valid():
                pm = MedicalPrescription(
                    med_consulation = mc,
                    #prescription_date = form.cleaned_data['prescription_date'],
                    expiration_date = form.cleaned_data['expiration_date'],
                    active_principle = form.cleaned_data['active_principle'],
                    dosage = form.cleaned_data['dosage'],
                    administration_route = form.cleaned_data['administration_route'],
                    container_format = form.cleaned_data['container_format'],
                    posology = form.cleaned_data['posology']
                )
                pm.save()
                dict['show_form'] = False
            else:
                dict['form'] = form
                dict['show_errors'] = True

        else:
            hoy = datetime.date.today()
            dict['today'] = hoy.strftime("%d/%m/%Y")
            venc = hoy + datetime.timedelta(days=30) #por defecto la receta prescrivira en 30 dias
            form_data = {'expiration_date': venc.strftime("%d/%m/%Y") }
            form = my_forms.MedicalPrescriptionForm(initial=form_data)
            dict['form'] = form

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_show_patient_prescription(request, id_pm):
    """
        Mostrar la receta medica
    """
    mi_template = get_template('Medics/GestionTurnos/mostrar-receta-medica.html')
    dict = generate_base_keys(request)

    if True:
        pm = MedicalPrescription.objects.get(id=id_pm)
        dict['pm'] = pm
        dict['pinfo'] = UserInformation.objects.get(user=pm.med_consulation.patient)
        dict['minfo'] = UserInformation.objects.get(user=pm.med_consulation.medic)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medical_prescription_pdf(request, id_pm):
    """
        Exporta la receta a PDF
    """
    if True:
        try:
            pm = MedicalPrescription.objects.get(id=id_pm)
            pac = UserInformation.objects.get(user=pm.med_consulation.patient)
            med = UserInformation.objects.get(user=pm.med_consulation.medic)
        except:
            path = request.META['PATH_INFO']
            return HttpResponseRedirect("/restricted-access%s" %path)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="receta.pdf"'

        reports.generate_medical_presc(response, pm, med, pac)
        return response



    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)


#def medic_del_patient_prescription(request, patient):
    #mi_template = get_template('Medics/GestionTurnos/listado-archivos.html')
    #dict = generate_base_keys(request)

    #if True:
        #pass

    #else:
        #path = request.META['PATH_INFO']
        #return HttpResponseRedirect("/restricted-access%s" %path)

    #html_cont = mi_template.render(Context(dict))
    #return HttpResponse(html_cont)



def medic_new_turn_day_select(request, pac_id, month=None, year=None):
    """
        vista del medico para selecionar un nuevo turno paciente
    """
    mi_template = get_template('Medics/GestionTurnos/new-turn-date-select.html')
    dict = generate_base_keys(request)
    
    # parche aplicacion por alguna razon el parseo de la expresion regular en  
    # urls.py no funciona correctamente esto es una correcion temporal hasta
    # que encuentre una expresion que funcione correctamente
    lst = pac_id.split('/')
    if len(lst) == 3:
        pac_id = lst[0]
        month = lst[1]
        year = lst[2]

    print pac_id

    dict['pac_username'] = pac_id #en este caso hace referencia al nombre de usuario

    if True:
        ## correcion de la fecha y de los spin para cambio de fechas ##
        if month != None and year != None:
            month = int(month) % 13
            year = int(year)

        else:
            year = datetime.date.today().year
            month = datetime.date.today().month

        #hoy
        t_day = datetime.date.today().day #dia
        t_year = datetime.date.today().year #mes
        t_month = datetime.date.today().month #anio

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

        #correcion para no mostrar los meses anteriores al mes actual
        if dict['prev_month'] < t_month and dict['prev_year'] == t_year or dict['prev_year'] < t_year:
            dict['prev_month'] = t_month
            dict['prev_year'] = t_year
        ## fin correcion fechas
        
        dict['patient'] = User.objects.get(username=pac_id)
        medic = UserInformation.objects.get(user=request.user)
        dict['medic'] = medic
        ## diferentes grupos segun patrones para armar el calendar ##
        #dias que se atiende
        bh = BusinessHours.objects.filter(user=medic.user)
        wd = []
        for day in bh:
            wd.append(day.date - 1)

        #dias no laborales
        nwd = NonWorkingDay.objects.filter(user=medic.user, date__month=month, date__year=year)
        _nwd = []
        for obj in nwd:
            _nwd.append(obj.date.day)

        #dias con turnos asignados
        _dta = []
        dof = DayOfAttention.objects.filter(business_hour__user=medic.user, date__month=month, date__year=year)
        for day in dof:
            if day.status == 2: #marcado como completo
                _dta.append(day.date - 1)

        #formateo del mes
        semanas = []
        for week in wekends:
            sem = []
            i = 0
            for day in week:
                if day in _nwd: #es un dia no laboral? dias precancelados por el medico
                    sem.append(CalendarDay(day,2))
                else:
                    if i in wd:#dias donde se atiende
                        #estan completos los dia de atencion
                        if day in _dta:
                            sem.append(CalendarDay(day,3))

                        #si paso la fecha de atencion se marcara como completo en la vista
                        elif day <= t_day and t_month == month and t_year == year:
                            sem.append(CalendarDay(day,3))
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



def medic_new_turn(request, pac_id, day, month, year):
    mi_template = get_template('Medics/GestionTurnos/new-turn.html')
    dict = generate_base_keys(request)

    if True:
        medic = UserInformation.objects.get(user=request.user)
        patient = User.objects.get(id=pac_id) 
        dict['patient'] = patient 
        dict['pac_username'] = patient.username
        dict['medic'] = medic

        if request.method == 'POST':
            key = str(medic.user.id) + day + month + year
            fkey = get_POST_value(request, 'key')
            if key == fkey:#datos
                ## consulta si es un dia valido
                str_d = day + '-' + month + '-' + year #formatea un string como dd-mm-aaaa
                s_day = dia_fecha(str_d) #nro de dia de la semana
                result = BusinessHours.objects.filter(user = medic.user, date=s_day).count()
                if result == 1:
                    ## consulta si tiene turnos disponible el dia
                    bh = BusinessHours.objects.get(user = medic.user, date=s_day)
                    _date = datetime.date(int(year),int(month),int(day))
                    is_turn = True #bandera de consulta asignacion de turno
                    try:
                        doa = DayOfAttention.objects.get(business_hour=bh, date=_date)

                    except DayOfAttention.DoesNotExist:
                        doa = DayOfAttention(
                            business_hour = bh,
                            date = _date,
                            status = 0,
                            number_of_turns = 0,
                            current_end_time = bh.start_time
                        )
                        doa.save()

                    if doa.number_of_turns > doa.business_hour.number_of_turns():
                        doa.status = 2 #esta completo de antemano no puede solicitar turno
                        is_turn = False #ya no se puede asignar turno

                    elif doa.number_of_turns == (doa.business_hour.number_of_turns() - 1):
                        doa.status = 2 #ulimo turno que se asignara
                        doa.number_of_turns += 1

                    else:
                        doa.status = 1
                        doa.number_of_turns += 1

                    _start = doa.current_end_time
                    _end = doa.get_next_current_end_time()
                    doa.current_end_time = doa.get_next_current_end_time()

                    if is_turn: #consulta bandera de registracion de turno
                        dict['not_errors'] = True
                        try:
                             #lanza un error en caso que se haya registrado un turno previamente en la misma fecha
                            #con el mismo especialista
                            turn = Turn.objects.get(medic=medic.user, patient=patient, day = doa)
                            if turn.status == 3: #reactivar turno previamente cancelado
                                turn.status = 0 #cambia a pendiente
                                turn.save()
                                dict['turn'] = turn

                            else:
                                dict['errors'] = 'No se pudo registrar el turno, por que ya posee un turno registrado esta fecha con dicho especialista'
                                dict['not_errors'] = False

                        except Turn.DoesNotExist:
                            #no hay un turno previo registrado
                            turn = Turn(
                                day = doa, #dia de atencion al cual esta relacionado
                                medic = medic.user,
                                patient = patient, #se supone que el paciente es el user actual logueado
                                start = _start,
                                end = _end,
                                status = 0,
                                observation = '',
                                number = doa.number_of_turns
                            )
                            turn.save()
                            doa.save()
                            dict['turn'] =turn

                    else:
                        dict['not_errors'] = False
                        dict['errors'] = 'Lo sentimos pero la fecha' + str(doa.date) + 'no tiene turnos disponibles'

                else:
                    dict['not_errors'] = False
                    dict['errors'] = 'El dia solicitado es invalido'

            else:
                dict['not_errors'] = False
                dict['errors'] = 'La clave de comprobacion no coincide'

        else:
            dict['show_form'] = True
            dict['key'] = str(medic.user.id) + day + month + year
            dict['date_str'] = day + ' de ' +  MONTHS[int(month)-1] + ' de ' + year

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def medic_show_patient_turn_request(request, pac_username):
    mi_template = get_template('Medics/GestionTurnos/show-turns-request.html')
    dict = generate_base_keys(request)

    if True:
        user = User.objects.get(username=pac_username)
        dict['patient'] = user
        dict['pac_username'] = user.username

        t_stat = [1,2,3,4,5]
        #status = 0 turno pendiente
        dict['p_turns'] = Turn.objects.filter(patient=user, status=0).order_by('day__date')
        dict['c_turns'] = Turn.objects.filter(patient=user, status__in=t_stat).order_by('day__date')

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def medic_show_patient_turn_detail(request, turn_id):
    mi_template = get_template('Medics/GestionTurnos/show-turn-detail.html')
    dict = generate_base_keys(request)

    if have_acess(request):
        user = request.user
        try: 
            turn = Turn.objects.get(id=turn_id, medic=request.user)
            dict['turn'] = turn 
            dict['pac_username'] = turn.patient.username

        except:
            path = request.META['PATH_INFO']
            return HttpResponseRedirect("/restricted-access%s" %path)

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)


def medic_turn_cancel(request, turn_id):
    """
        Vista para cancelar los turnos pendientes.
    """
    mi_template = get_template('Medics/GestionTurnos/cancel-turn.html')
    dict = generate_base_keys(request)
    if True:
        user = request.user
        try:
            turn = Turn.objects.get(id=turn_id)#, patient=request.user)
            dict['turn'] = turn
            dict['pac_username'] = turn.patient.username

        except:
            path = request.META['PATH_INFO']
            return HttpResponseRedirect("/restricted-access%s" %path)

        dict['show_turn'] = True

        if request.method == "POST":
            dict['show_turn'] = False
            turn.status = 2 #cancelado por medico
            turn.save()

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

 
def medic_turn_reset(request, turn_id):
    """
        Reactiva un turno cancelado siempre y cuando el mismo no haya caducado
    """
    mi_template = get_template('Medics/GestionTurnos/turn-reset.html')
    dict = generate_base_keys(request)

    if have_acess(request):
        try: 
            turn = Turn.objects.get(id=turn_id)
            dict['pac_username'] = turn.patient.username
            
            today = datetime.date.today() #hoy
            #si la fecha del turno es mayor significa que no expiro y que puede
            #ser reactivado
            if turn.day.date >= today:
                turn.status = 0
                turn.observation = ""
                turn.save()
                dict['turn_valid'] = True
                dict['turn_id'] = turn.id

            else:
                dict['turn_valid'] = False

        except:
            path = request.META['PATH_INFO']
            return HttpResponseRedirect("/restricted-access%s" %path)

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)
