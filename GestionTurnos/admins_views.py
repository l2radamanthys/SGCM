# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth #para login
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as DjangoGroup

#from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from GestionTurnos.models import *
import GestionTurnos.forms as myforms
from utils import *
import verbose
import forms as my_forms
from globals import *
import HTMLTags as Tags




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
        #dict['iuser_lbl'] = iuser.
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



def admin_show_admin(request):
    pass



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



def admin_edit_patient_info(request, pac_id):
    pass



def admin_search_patient(request):
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



def admin_select_medic_for_patient(request, pac_id):
    pass



def admin_select_date_medic_turn(request, pac_id, med_id, date):
    pass



def admin_add_medic_turn(request, pac_id, med_id, date):
    pass



def admin_cancel_medic_turn(request, turn_id):
    pass



#estadisticas pensar
#def admin_show_