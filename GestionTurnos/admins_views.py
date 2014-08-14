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
import GestionTurnos.forms as myforms
from utils import *
#import verbose
import calendar
import datetime
import forms as my_forms
from globals import *
import HTMLTags as Tags
import my_forms as globals_forms
import reports


def admin_add_medic(request):
    """
        Registrar Medico
    """
    mi_template = get_template('Admins/GestionTurnos/registrar-medico.html')
    dict = generate_base_keys(request)
    if True:
        dict['show_form'] = True
        dict['show_erros'] = False
        if request.method == "POST":
            uform = myforms.UserRegForm(request.POST)
            dform = myforms.RegMedicInformationForm(request.POST)
            if uform.is_valid() and dform.is_valid():

                _username = uform.cleaned_data['username']
                try:
                    _user = User.objects.get(username=_username)
                    dict['show_errors'] = True
                    dict['custon_errors'] = Tags.html_message("Error el usuario %s ya existe.." %Tags.strong(_username))
                    dict['uform'] = uform
                    dict['dform'] = dform

                except User.DoesNotExist:
                    _password = uform.cleaned_data['password']
                    _email = uform.cleaned_data['email']
                    _user = User.objects.create_user(username=_username, email=_email, password=_password)
                    _user.first_name = uform.cleaned_data['first_name']
                    _user.last_name = uform.cleaned_data['last_name']
                    _user.is_staff = False #no es admin
                    _user.is_active = True #esta activo despues cambio, para hacer algun modo de activacion
                    group = DjangoGroup.objects.get(name='Medico')
                    _user.groups.add(group)
                    _user.save()
                    info = UserInformation(
                        user = _user,
                        type_doc = dform.cleaned_data['type_doc'],
                        nro_doc = dform.cleaned_data['nro_doc'],
                        gender = dform.cleaned_data['gender'],
                        phone = dform.cleaned_data['phone'],
                        address = dform.cleaned_data['address'],
                        city = dform.cleaned_data['city'],
                        state = dform.cleaned_data['state'],
                        birth_date = dform.cleaned_data['birth_date'],
                        matricula = dform.cleaned_data['matricula']
                    )
                    info.save()
                    dict['show_form'] = False
                    dict['custom_message'] = Tags.html_message("Medico <strong>%s</strong> Registrado Correctamente.."  %(uform.cleaned_data['first_name']+" "+uform.cleaned_data['last_name']), type="ok")

            else:
                dict['show_errors'] = True
                dict['uform'] = uform
                dict['dform'] = dform

        else:
            dict['uform'] =  myforms.UserRegForm()
            dict['dform'] = myforms.RegMedicInformationForm()

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_search_medic(request):
    """
        Buscar Medicos
    """
    mi_template = get_template('Admins/GestionTurnos/buscar-usuarios.html')
    dict = generate_base_keys(request)

    if True:
        #conf
        type = "Medico"
        dict['type_user'] = 'Medico'
        dict['url_dest'] = '/admins/mostrar/medico/'

        field = get_value(request, 'field')
        argv = get_value(request, 'search')

        if field == 'u':
            dict['search_result'] = User.objects.filter(groups__name=type, username__contains=argv)
        elif field == 'n':
            dict['search_result'] = User.objects.filter(groups__name=type, first_name__contains=argv)
        elif field == 'a':
            dict['search_result'] = User.objects.filter(groups__name=type, last_name__contains=argv)
        else:
            dict['search_result'] = User.objects.filter(groups__name=type)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_show_medic(request, med_id):
    mi_template = get_template('Admins/GestionTurnos/medic-view.html')
    dict = generate_base_keys(request)

    if True:
        iuser = User.objects.get(username=med_id)
        dict['expecialidades'] = MedicalSpecialityFor.objects.filter(user=iuser)
        dict['iuser'] = iuser
        dict['is_medic'] = True
        dict['info'] = UserInformation.objects.get(user=iuser)


    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_edit_medic_info(request, med_id):
    pass



def admin_delete_medic(request):
    pass




def admin_add_medic_expeciality(request, med_id, exp_id=None):
    mi_template = get_template('Admins/GestionTurnos/medic-add-expeciality.html')
    dict = generate_base_keys(request)

    if True:
        dict['show_form'] = True
        dict['show_errors'] = False
        med = User.objects.get(username=med_id)
        dict['med'] = med
        dict['iuser'] = med

        if request.method == 'POST':
            form = my_forms.MedicalSpecialtyForForm(request.POST)
            if form.is_valid():
                print form.cleaned_data['expecialidad']
                expf =  MedicalSpecialityFor(
                    user=med,
                    speciality = MedicalSpecialties.objects.get(id=get_value(request,'expecialidad'))
                )
                expf.save()
                #dict['show_form'] = False
                #dict['show_errors'] = False
                return HttpResponseRedirect("/admins/mostrar/medico/%s/" %med.username)
            else:
                dict['form'] = form
                dict['show_errors'] = True
        else:
            dict['form'] = my_forms.MedicalSpecialtyForForm()

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_add_admin(request):
    """
        Registrar Administrativo
    """
    mi_template = get_template('Admins/GestionTurnos/registrar-admin.html')
    dict = generate_base_keys(request)
    if True:
        dict['show_form'] = True
        dict['show_erros'] = False
        if request.method == "POST":
            uform = myforms.UserRegForm(request.POST)
            dform = myforms.RegAdminInformationForm(request.POST)
            if uform.is_valid() and dform.is_valid():

                _username = uform.cleaned_data['username']
                try:
                    user = User.objects.get(username=_username)
                    dict['show_errors'] = True
                    dict['custon_errors'] = Tags.html_message("Error el usuario %s ya existe.." %Tags.strong(_username))
                    dict['uform'] = uform
                    dict['dform'] = dform

                except User.DoesNotExist:
                    _password = uform.cleaned_data['password']
                    _email = uform.cleaned_data['email']
                    _user = User.objects.create_user(username=_username, email=_email, password=_password)
                    _user.first_name = uform.cleaned_data['first_name']
                    _user.last_name = uform.cleaned_data['last_name']
                    _user.is_staff = True #es admin
                    _user.is_active = True #esta activo despues cambio, para hacer algun modo de activacion
                    group = DjangoGroup.objects.get(name='Administrativo')
                    _user.groups.add(group)
                    _user.save()
                    info = UserInformation(
                        user = _user,
                        type_doc = dform.cleaned_data['type_doc'],
                        nro_doc = dform.cleaned_data['nro_doc'],
                        gender = dform.cleaned_data['gender'],
                        phone = dform.cleaned_data['phone'],
                        address = dform.cleaned_data['address'],
                        city = dform.cleaned_data['city'],
                        state = dform.cleaned_data['state'],
                        birth_date = dform.cleaned_data['birth_date'],
                    )
                    info.save()
                    dict['show_form'] = False
                    dict['custom_message'] = Tags.html_message("Administrativo <strong>%s</strong> Registrado Correctamente.."  %(uform.cleaned_data['first_name']+" "+uform.cleaned_data['last_name']), type="ok")

            else:
                dict['show_errors'] = True
                dict['uform'] = uform
                dict['dform'] = dform

        else:
            dict['uform'] =  myforms.UserRegForm()
            dict['dform'] = myforms.RegAdminInformationForm()

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_search_admin(request):
    mi_template = get_template('Admins/GestionTurnos/buscar-usuarios.html')
    dict = generate_base_keys(request)

    if True:
        #conf
        type = "Administrativo"
        dict['type_user'] = 'Administrativo'
        dict['url_dest'] = '/admins/mostrar/administrativo/'

        field = get_value(request, 'field')
        argv = get_value(request, 'search')

        if field == 'u':
            dict['search_result'] = User.objects.filter(groups__name=type, username__contains=argv)
        elif field == 'n':
            dict['search_result'] = User.objects.filter(groups__name=type, first_name__contains=argv)
        elif field == 'a':
            dict['search_result'] = User.objects.filter(groups__name=type, last_name__contains=argv)
        else:
            dict['search_result'] = User.objects.filter(groups__name=type)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_show_admin(request, adm_id):
    mi_template = get_template('Admins/GestionTurnos/admin-view.html')
    dict = generate_base_keys(request)

    if True:
        iuser = User.objects.get(username=adm_id)
        dict['expecialidades'] = MedicalSpecialityFor.objects.filter(user=iuser)
        dict['iuser'] = iuser
        #dict['iuser_lbl'] = iuser.
        dict['info'] = UserInformation.objects.get(user=iuser)


    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_delete_admin(request):
    pass



def admin_add_expeciality(request):
    mi_template = get_template('Admins/GestionTurnos/agregar-expecialidad.html')
    dict = generate_base_keys(request)

    if True:
        dict['show_form'] = True
        dict['show_errors'] = False
        if request.method == 'POST':
            form = my_forms.MedicalSpecialtiesForm(request.POST)
            if form.is_valid():
                exp = MedicalSpecialties(
                    name = form.cleaned_data['name'],
                    description = form.cleaned_data['description']
                )
                exp.save()
                #dict['show_form'] = False
                #dict['show_errors'] = False
                return HttpResponseRedirect("/admins/listado/expecialidad-medica/")
            else:
                dict['form'] = form
                dict['show_errors'] = True
        else:
            dict['form'] = my_forms.MedicalSpecialtiesForm()
    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_show_expeciality(request, exp_id):
    """
        Es generico para ver la informacion sobre la expecialidad
        en particular
    """
    mi_template = get_template('Admins/GestionTurnos/mostrar-expecialidad.html')
    dict = generate_base_keys(request)

    if True:
        dict['exp'] = MedicalSpecialties.objects.get(id=exp_id)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_list_expecialities(request):
    mi_template = get_template('Admins/GestionTurnos/listado-expecialidades.html')
    dict = generate_base_keys(request)

    if True:
        dict['expecialidades'] = MedicalSpecialties.objects.all()

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_add_patient(request):
    """
        Implementado
    """
    pass



def admin_search_patient(request):
    mi_template = get_template('Admins/GestionTurnos/buscar-usuarios.html')
    dict = generate_base_keys(request)

    if True:
        #conf
        type = "Paciente"
        dict['type_user'] = 'Paciente'
        dict['url_dest'] = '/admins/mostrar/paciente/'

        field = get_value(request, 'field')
        argv = get_value(request, 'search')

        if field == 'u':
            dict['search_result'] = User.objects.filter(groups__name=type, username__contains=argv)
        elif field == 'n':
            dict['search_result'] = User.objects.filter(groups__name=type, first_name__contains=argv)
        elif field == 'a':
            dict['search_result'] = User.objects.filter(groups__name=type, last_name__contains=argv)
        else:
            dict['search_result'] = User.objects.filter(groups__name=type)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_show_patient(request, pac_id):
    mi_template = get_template('Admins/GestionTurnos/patient-view.html')
    dict = generate_base_keys(request)

    if True:
        iuser = User.objects.get(username=pac_id)
        dict['expecialidades'] = MedicalSpecialityFor.objects.filter(user=iuser)
        dict['iuser'] = iuser
        dict['info'] = UserInformation.objects.get(user=iuser)
        dict['turns'] = Turn.objects.filter(patient=iuser)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_update_patient_turn(request, turn_id):
    mi_template = get_template('Admins/GestionTurnos/turn-edit.html')
    dict = generate_base_keys(request)

    if have_acess(request, ['admin']):
        turn = Turn.objects.get(id=int(turn_id))
        dict['turn'] = turn
        iuser = turn.patient
        dict['iuser'] = iuser

        if request.method == 'POST':
            form = myforms.TurnEditForm(request.POST)
            if form.is_valid():
                turn.status = form.cleaned_data['status']
                turn.observation = form.cleaned_data['observation']
                turn.save()

                dict['show_form'] = False
                dict['turn_id'] = turn.id

            else:
                dict['form'] = form
                dict['show_form'] = True

        else:
            fdata = {'observation': turn.observation, 'status': turn.status}
            dict['form'] = myforms.TurnEditForm(fdata)
            dict['show_form'] = True

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_update_medic_turn(request, turn_id):
    mi_template = get_template('Admins/GestionTurnos/turn-edit-medic.html')
    dict = generate_base_keys(request)

    if have_acess(request, ['admin']):
        turn = Turn.objects.get(id=int(turn_id))
        dict['turn'] = turn
        iuser = turn.patient
        dict['iuser'] = iuser

        if request.method == 'POST':
            form = myforms.TurnEditForm(request.POST)
            if form.is_valid():
                turn.status = form.cleaned_data['status']
                turn.observation = form.cleaned_data['observation']
                turn.save()

                dict['show_form'] = False
                dict['turn_id'] = turn.id

            else:
                dict['form'] = form
                dict['show_form'] = True

        else:
            fdata = {'observation': turn.observation, 'status': turn.status}
            dict['form'] = myforms.TurnEditForm(fdata)
            dict['show_form'] = True

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



#def admin_show_patient_turn(request, turn_id):
#    mi_template = get_template('Admins/GestionTurnos/show-turn-patient.html')


def admin_show_patient_turn(request, turn_id):
    mi_template = get_template('Admins/GestionTurnos/show-turn-patient.html')
    dict = generate_base_keys(request)

    if have_acess(request, ['admin']):
        turn = Turn.objects.get(id=int(turn_id))
        dict['turn'] = turn
        iuser = turn.patient
        dict['iuser'] = iuser

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)


def admin_show_medic_turn(request, turn_id):
    mi_template = get_template('Admins/GestionTurnos/show-turn-medic.html')
    dict = generate_base_keys(request)

    if have_acess(request, ['admin']):
        turn = Turn.objects.get(id=int(turn_id))
        dict['turn'] = turn
        iuser = turn.patient
        dict['iuser'] = iuser

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)




def admin_edit_patient(request, pac_id):
    mi_template = get_template('Admins/GestionTurnos/patient-edit.html')
    dict = generate_base_keys(request)

    if True:
        dict['show_form'] = True
        dict['show_errors'] = False
        user = User.objects.get(username=pac_id)
        user_data = UserInformation.objects.get(user=user)
        dict['iuser'] = user

        form_user_data = {
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'email' : user.email,
        }

        form_info_data = {
            'type_doc': user_data.type_doc,
            'nro_doc': user_data.nro_doc,
            'gender': user_data.gender,
            'phone': user_data.phone,
            'address': user_data.address,
            'city': user_data.city,
            'state': user_data.state,
            'birth_date': user_data.birth_date.strftime("%d/%m/%Y"),
        #es paciente no interesa la matricula
        #    'matricula': user_data.matricula,
        }

        if request.method == 'POST':
            form_user = globals_forms.ChangeUserDataForm(request.POST)
            form_info = globals_forms.ChangeUserInformationForm(request.POST)
            if form_user.is_valid() and form_info.is_valid():
                user.first_name = form_user.cleaned_data['first_name']
                user.last_name = form_user.cleaned_data['last_name']
                user.email = form_user.cleaned_data['email']
                user.save()

                user_data.type_doc = form_info.cleaned_data['type_doc']
                user_data.nro_doc = form_info.cleaned_data['nro_doc']
                user_data.gender = form_info.cleaned_data['gender']
                user_data.phone = form_info.cleaned_data['phone']
                user_data.address = form_info.cleaned_data['address']
                user_data.city = form_info.cleaned_data['city']
                user_data.state = form_info.cleaned_data['state']
                user_data.birth_date = form_info.cleaned_data['birth_date']
                user_data.save()

                return HttpResponseRedirect("/admins/mostrar/paciente/%s/" %user.username)
            else:
                dict['show_errors'] = True
                dict['form_user'] = form_user
                dict['form_info'] = form_info

        else:
            dict['form_user'] = globals_forms.ChangeUserDataForm(initial=form_user_data)
            dict['form_info'] = globals_forms.ChangeUserInformationForm(initial=form_info_data)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_edit_admin(request, adm_id):
    mi_template = get_template('Admins/GestionTurnos/admin-edit.html')
    dict = generate_base_keys(request)

    if True:
        dict['show_form'] = True
        dict['show_errors'] = False
        user = User.objects.get(username=adm_id)
        user_data = UserInformation.objects.get(user=user)
        dict['iuser'] = user

        form_user_data = {
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'email' : user.email,
        }

        form_info_data = {
            'type_doc': user_data.type_doc,
            'nro_doc': user_data.nro_doc,
            'gender': user_data.gender,
            'phone': user_data.phone,
            'address': user_data.address,
            'city': user_data.city,
            'state': user_data.state,
            'birth_date': user_data.birth_date.strftime("%d/%m/%Y"),
        #es paciente no interesa la matricula
        #    'matricula': user_data.matricula,
        }

        if request.method == 'POST':
            form_user = globals_forms.ChangeUserDataForm(request.POST)
            form_info = globals_forms.ChangeUserInformationForm(request.POST)
            if form_user.is_valid() and form_info.is_valid():
                user.first_name = form_user.cleaned_data['first_name']
                user.last_name = form_user.cleaned_data['last_name']
                user.email = form_user.cleaned_data['email']
                user.save()

                user_data.type_doc = form_info.cleaned_data['type_doc']
                user_data.nro_doc = form_info.cleaned_data['nro_doc']
                user_data.gender = form_info.cleaned_data['gender']
                user_data.phone = form_info.cleaned_data['phone']
                user_data.address = form_info.cleaned_data['address']
                user_data.city = form_info.cleaned_data['city']
                user_data.state = form_info.cleaned_data['state']
                user_data.birth_date = form_info.cleaned_data['birth_date']
                user_data.save()

                return HttpResponseRedirect("/admins/mostrar/administrativo/%s/" %user.username)
            else:
                dict['show_errors'] = True
                dict['form_user'] = form_user
                dict['form_info'] = form_info

        else:
            dict['form_user'] = globals_forms.ChangeUserDataForm(initial=form_user_data)
            dict['form_info'] = globals_forms.ChangeUserInformationForm(initial=form_info_data)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_change_patient_password(request, pac_id):
    mi_template = get_template('Admins/GestionTurnos/patient-change-password.html')
    dict = generate_base_keys(request)

    if True:
        iuser = User.objects.get(username=pac_id)
        dict['iuser'] = iuser

        if request.method == "POST":
            pswd = get_value(request, 'password')
            iuser.set_password(pswd)
            iuser.save()

        else:
            dict['show_form'] = True
    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_patient_turn_set_medic(request, pac_id):
    mi_template = get_template('Admins/GestionTurnos/patient-turn-medic-select.html')
    dict = generate_base_keys(request)

    if True:
        iuser = User.objects.get(username=pac_id)
        dict['iuser'] = iuser
        dict['medics'] = User.objects.filter(groups__name="Medico")

        if request.method == "POST":
            _url = "/admins/selecionar-dia/turno/%s/%s/" %(iuser.username, get_value(request, 'medic'))
            return HttpResponseRedirect(_url)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)


def admin_select_date_medic_turn(request, pac_id, med_id, month=None, year=None):
    mi_template = get_template('Admins/GestionTurnos/new-turn-date-select.html')
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

        patient = User.objects.get(username=pac_id)
        dict['patient'] = patient
        dict['iuser'] = patient
        medic = UserInformation.objects.get(user__username=med_id)
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

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)




def admin_new_turn(request, pac_id, med_id, day, month, year):
    mi_template = get_template('Admins/GestionTurnos/new-turn.html')
    dict = generate_base_keys(request)

    if True:
        medic = UserInformation.objects.get(user__username=med_id)
        patient = User.objects.get(username=pac_id)
        dict['patient'] = patient
        dict['iuser'] = patient
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



def admin_delete_medic_expeciality(request, med_id, exp_id):
    """
        Esto no tiene vista especifica por que directamente o borrara la
        expecialidad o levantara un error
    """
    if have_acess(request, ['admin']):
        try:
            expmed = MedicalSpecialityFor.objects.get(user__username=med_id, id=int(exp_id))
            expmed.delete()
            return HttpResponseRedirect("/admins/mostrar/medico/%s/" %med_id)

        except:
            path = request.META['PATH_INFO']
            return HttpResponseRedirect("/restricted-access%s" %path)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def admin_change_medic_password(request, med_id):
    mi_template = get_template('Admins/GestionTurnos/medic-change-password.html')
    dict = generate_base_keys(request)

    if True:
        iuser = User.objects.get(username=med_id)
        dict['iuser'] = iuser

        if request.method == "POST":
            pswd = get_value(request, 'password')
            iuser.set_password(pswd)
            iuser.save()

        else:
            dict['show_form'] = True
    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_change_admin_password(request, adm_id):
    mi_template = get_template('Admins/GestionTurnos/admin-change-password.html')
    dict = generate_base_keys(request)

    if True:
        iuser = User.objects.get(username=adm_id)
        dict['iuser'] = iuser

        if request.method == "POST":
            pswd = get_value(request, 'password')
            iuser.set_password(pswd)
            iuser.save()

        else:
            dict['show_form'] = True
    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def admin_show_medic_turn_list(request, med_id):
    mi_template = get_template('Admins/GestionTurnos/medic-listado-turnos.html')
    dict = generate_base_keys(request)

    if True:
        dict['turns'] = Turn.objects.filter(medic__username=med_id)
        iuser = User.objects.get(username=med_id)
        dict['iuser'] = iuser

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)


def turn_pdf(request, turn_id):
    """
    """
    #mi_template = get_template('Patients/GestionTurnos/show-turn-detail.html')
    #dict = generate_base_keys(request)
    if have_acess(request, ['medic', 'patient']):
        try:
            turn = Turn.objects.get(id=turn_id)

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



def admin_edit_medic(request, med_id):
    """
        Administrativo, modificar datos del medico
    """
    mi_template = get_template('Admins/GestionTurnos/medic-edit.html')
    dict = generate_base_keys(request)

    if True:
        dict['show_form'] = True
        dict['show_errors'] = False
        user = User.objects.get(username=med_id)
        user_data = UserInformation.objects.get(user=user)
        dict['iuser'] = user

        form_user_data = {
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'email' : user.email,
        }

        form_info_data = {
            'type_doc': user_data.type_doc,
            'nro_doc': user_data.nro_doc,
            'gender': user_data.gender,
            'phone': user_data.phone,
            'address': user_data.address,
            'city': user_data.city,
            'state': user_data.state,
            'birth_date': user_data.birth_date.strftime("%d/%m/%Y"),
            'matricula': user_data.matricula,
        }

        if request.method == 'POST':
            form_user = globals_forms.ChangeUserDataForm(request.POST)
            form_info = globals_forms.ChangeMedicInformationForm(request.POST)
            if form_user.is_valid() and form_info.is_valid():
                user.first_name = form_user.cleaned_data['first_name']
                user.last_name = form_user.cleaned_data['last_name']
                user.email = form_user.cleaned_data['email']
                user.save()

                user_data.type_doc = form_info.cleaned_data['type_doc']
                user_data.nro_doc = form_info.cleaned_data['nro_doc']
                user_data.gender = form_info.cleaned_data['gender']
                user_data.phone = form_info.cleaned_data['phone']
                user_data.address = form_info.cleaned_data['address']
                user_data.city = form_info.cleaned_data['city']
                user_data.state = form_info.cleaned_data['state']
                user_data.birth_date = form_info.cleaned_data['birth_date']
                user_data.matricula = form_info.cleaned_data['matricula']
                user_data.save()

                return HttpResponseRedirect("/admins/mostrar/medico/%s/" %user.username)
            else:
                dict['show_errors'] = True
                dict['form_user'] = form_user
                dict['form_info'] = form_info

        else:
            dict['form_user'] = globals_forms.ChangeUserDataForm(initial=form_user_data)
            dict['form_info'] = globals_forms.ChangeMedicInformationForm(initial=form_info_data)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)


