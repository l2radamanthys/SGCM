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
import calendar
import datetime

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




def patient_show_medics_list(request):
    """
    Muestra el listado de Medicos
    """
    mi_template = get_template('Patients/GestionTurnos/medics-list.html')
    dict = generate_base_keys(request)

    if True:
        dict['medics'] = UserInformation.objects.filter(user__groups__name='Medico')
        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        #si hay un usuario logueado intentanto acceder sera enviado a una
        #pagina de error
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def patient_show_medic_info(request, med_id):
    """
    Muestra informacion acerca del medico
    """
    mi_template = get_template('Patients/GestionTurnos/show-medic-info.html')
    dict = generate_base_keys(request)

    if True:
        dict['medic'] = UserInformation.objects.get(user__id=med_id)
        dict['expecialities'] = MedicalSpecialityFor.objects.filter(user__id=med_id)
        dict['business_hours'] = BusinessHours.objects.filter(user__id=med_id)
        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        #si hay un usuario logueado intentanto acceder sera enviado a una
        #pagina de error
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def patient_new_turn_day_select(request, med_id, month=None, year=None):
    """
        vista para selecionar un nuevo turno paciente
    """
    mi_template = get_template('Patients/GestionTurnos/new-turn-date-select.html')
    dict = generate_base_keys(request)

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

        medic = UserInformation.objects.get(user__id=med_id)
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
                        elif day <= t_day and t_month == month:
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


def patient_new_turn(request, med_id, day, month, year):
    mi_template = get_template('Patients/GestionTurnos/new-turn.html')
    dict = generate_base_keys(request)

    if True:
        medic = UserInformation.objects.get(user__id=med_id)
        dict['medic'] = medic

        if request.method == 'POST':
            key = med_id + day + month + year
            fkey = get_POST_value(request, 'key')
            if key == fkey:#datos
                ## consulta si es un dia valido
                str_d = day + '-' + month + '-' + year #formatea un string como dd-mm-aaaa
                s_day = dia_fecha(str_d) #nro de dia de la semana
                result = BusinessHours.objects.filter(user__id = med_id, date=s_day).count()
                if result == 1:
                    ## consulta si tiene turnos disponible el dia
                    bh = BusinessHours.objects.get(user__id = med_id, date=s_day)
                    _date = datetime.date(int(year),int(month),int(day))
                    is_turn = True #bandera de consulta asignacion de turno
                    try:
                        doa = DayOfAttention.objects.get(business_hour=bh, date=_date)

                    except DayOfAttention.DoesNotExist:
                        doa = DayOfAttention(
                            business_hour = bh,
                            date = _date,
                            status = 0,
                            number_of_turns = 0
                        )

                    if doa.number_of_turns >= doa.business_hour.number_of_turns():
                        doa.status = 2 #esta completo de antemano no puede solicitar turno
                        is_turn = False #ya no se puede asignar turno

                    elif doa.number_of_turns == (doa.business_hour.number_of_turns() - 1):
                        doa.status = 2 #ulimo turno que se asignara
                        doa.number_of_turns += 1

                    else:
                        doa.number_of_turns += 1

                    if is_turn: #consulta bandera de registracion de turno
                        turn = Turn(
                            day = doa, #dia de atencion al cual esta relacionado
                            medic = medic.user,
                            patient = request.user, #se supone que el paciente es el user actual logueado
                            start = datetime.time(),
                            end = datetime.time(),
                            status = 0,
                            observation = '',
                            number = doa.number_of_turns
                        )
                        turn.save()
                        dict['turn'] =turn

                    else:
                        dict['errors'] = 'no hay turnos disponibles'

                    doa.save()


                else:
                    dict['errors'] = 'dia no valido'

            else:
                dict['errors'] = 'claves invalidas'

            pass
        else:
            dict['show_form'] = True
            dict['key'] = med_id + day + month + year
            dict['date_str'] = day + ' de ' +  MONTHS[int(month)-1] + ' de ' + year

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)