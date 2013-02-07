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



def search(request):
    """
    """
    mi_template = get_template('GestionTurnos/medico-buscar.html')
    dict = generate_base_keys(request)

    if request.user.has_perm('change_medic'):
        dict['modify'] = True

    dict['search_result'] = User.objects.filter(groups__name='Medicos')

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




def show_my_business_hours(request):
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



def add_my_business_hours(request):
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



def del_my_business_hours(request, bh_id):
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
	    pass

	#dict['business_hours'] = BusinessHours.objects.filter(user__username=request.user.username)

	html_cont = mi_template.render(Context(dict))
	return HttpResponse(html_cont)

    else:
	path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def show_medic_business_hours(request, id):
    """
        Muestra los horarios de Atencion del Medico
    """
    mi_template = get_template('GestionTurnos/Medics/medico-horarios-atencion.html')
    dict = generate_base_keys(request)

    id = int(id)
    user_ = User.objects.get(id=id)
    dict['user'] = user_
    dict['business_hours'] = BusinessHours.objects.filter(user=user_)

    if request.user.has_perm('change_medic'):
        dict['modify'] = True
    

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def add_medic_business_hours(request, id):
    """
        Agrega un Horario de Atencion a la Agenda del Medico

    Accesso:
    --------
        - Administradores
        - Medicos
    """
    mi_template = get_template('GestionTurnos/medico-horarios-atencion-nuevo.html')
    dict = generate_base_keys(request)

    user_ = User.objects.get(id=id)
    dict['user'] = user_

    if request.user.has_perm('change_medic'):

        if request.method == 'POST':
            dict['query'] = True
            form = my_forms.BusinessHoursForm(request.POST, auto_id=False)
            if form.is_valid():
                business_hour = BusinessHours(
                    user = user_,
                    date = form.cleaned_data['date'],
                    start_time = time_split(form.cleaned_data['start_time']),
                    end_time = time_split(form.cleaned_data['end_time']),
                    turn_duration = int(form.cleaned_data['turn_duration']),
                )
                business_hour.save()

            else:
                dict['form_error'] = form
        dict['form'] = my_forms.BusinessHoursForm()
        dict['business_hours'] = BusinessHours.objects.filter(user=user_)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def show_nonworking_days(request, month=None, year=None):
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

	#formateo del mes
	semanas = []
	for week in wekends:
	    sem = []
	    for day in week:
		sem.append(CalendarDay(day,1))
	    sem[5].type = 0
	    sem[6].type = 0
	    semanas.append(sem)
	   
	dict['wekends'] = semanas

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def add_nonworking_day(request, day, month, year):
    """
    """
    mi_template = get_template('Medics/GestionTurnos/dias-no-laborales.html')
    dict = generate_base_keys(request)

    if True:
	    pass

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def del_nonworking_day(request, day, month, year):
    """
    """
    mi_template = get_template('Medics/GestionTurnos/dias-no-laborales.html')
    dict = generate_base_keys(request)

    if True:
	    pass

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)