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
import reports


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
                    if False:
                        subject = "Confirmacion Registro Paciente"
                        to_email = user.email
                        #from_email = "registro-usuario@sgcm.com"
                        from settings import EMAIL_HOST_USER
                        from_email = EMAIL_HOST_USER
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
                    else:
                        user.is_active = True #el usuario deve ser activado mediante una confirmacion que se envia al mail
                        user.save()
                    dict['show_form'] = False
                    dict['custon_message'] = Tags.html_message("Paciente Registrado %s Correctamente.."  %(form.cleaned_data['first_name']), type="success")
                    #dict['query'] =  "user ok"
            else:
                dict['show_form'] = True #mostrar form de registro
                dict['show_errors'] = True
                dict['form_errors'] = True
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
                        user.is_active = True
                        user.save()
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

                    ## debug
                    #dict['test'] = bh.number_of_turns_bh(bh)
                    #dict['test'] = doa.number_of_turns
                    #dict['test'] = doa.get_next_current_end_time()
                    #dict['test'] = str(doa.number_of_turns) + " - "
                    #dict['test'] += str(_start) + "  - "
                    #dict['test'] += str(_end)


                    if is_turn: #consulta bandera de registracion de turno
                        dict['not_errors'] = True
                        try:
                             #lanza un error en caso que se haya registrado un turno previamente en la misma fecha
                            #con el mismo especialista
                            turn = Turn.objects.get(medic=medic.user, patient=request.user, day = doa)
                            if turn.status == 3: #reactivar turno previamente cancelado
                                turn.status = 0 #cambia a pendiente
                                turn.save()
                                dict['turn'] = turn

                            else:
                                dict['errors'] = 'No se pudo registrar el turno, por que ya posee un turno registrado esta fecha con dicho especialista'
                                dict['not_errors'] = False

                        except Turn.DoesNotExist:
                            turn = Turn(
                                day = doa, #dia de atencion al cual esta relacionado
                                medic = medic.user,
                                patient = request.user, #se supone que el paciente es el user actual logueado
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



def patient_set_medic_consulation(request, med_id):
    """
        Envia una consulta online a un medico, lo que en realidad es
        un mensaje
    """
    #no me acuerdo el nombre de consulta medica en ingles -.-
    mi_template = get_template('Patients/GestionTurnos/new-online-consulation.html')
    dict = generate_base_keys(request)

    if True:
        medic = UserInformation.objects.get(user__id=med_id)
        form = my_forms.OnlineConsulationForm()

        dict['medic'] = medic
        dict['show_form'] = True


        if request.method == 'POST':
            form = my_forms.OnlineConsulationForm(request.POST, auto_id=False)
            if form.is_valid():
                #to_user_id = form.cleaned_data['to_user']
                try:
                    _to_user = medic.user #el destinatario siempre sera el medico selecionado
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
            dict['form'] = my_forms.OnlineConsulationForm(auto_id=False)

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def patient_show_turn_request(request):
    mi_template = get_template('Patients/GestionTurnos/show-turns-request.html')
    dict = generate_base_keys(request)

    if True:
        user = request.user
        t_stat = [1,2,3,4,5]
        #status = 0 turno pendiente
        dict['p_turns'] = Turn.objects.filter(patient=user, status=0).order_by('day__date')
        dict['c_turns'] = Turn.objects.filter(patient=user, status__in=t_stat).order_by('day__date')


        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def patient_show_turn_detail(request, turn_id):
    mi_template = get_template('Patients/GestionTurnos/show-turn-detail.html')
    dict = generate_base_keys(request)

    if have_acess(request):
        user = request.user
        try:
            dict['turn'] = Turn.objects.get(id=turn_id, patient=request.user)

        except:
            path = request.META['PATH_INFO']
            return HttpResponseRedirect("/restricted-access%s" %path)

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)


def patient_turn_pdf(request, turn_id):
    """
    """
    #mi_template = get_template('Patients/GestionTurnos/show-turn-detail.html')
    #dict = generate_base_keys(request)
    if True:
        user = request.user
        try:
            turn = Turn.objects.get(id=turn_id, patient=request.user)

        except:
            path = request.META['PATH_INFO']
            return HttpResponseRedirect("/restricted-access%s" %path)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="turno.pdf"'
        reports.generate_turn(response, turn)
        return response

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def patient_turn_cancel(request, turn_id):
    """
        Vista para cancelar los turnos pendientes.
    """
    mi_template = get_template('Patients/GestionTurnos/cancel-turn.html')
    dict = generate_base_keys(request)
    if True:
        user = request.user
        try:
            turn = Turn.objects.get(id=turn_id, patient=request.user)
            dict['turn'] = turn

        except:
            path = request.META['PATH_INFO']
            return HttpResponseRedirect("/restricted-access%s" %path)

        dict['show_turn'] = True

        if request.method == "POST":
            dict['show_turn'] = False
            turn.status = 3 #cancelado paciente
            turn.save()

        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)
