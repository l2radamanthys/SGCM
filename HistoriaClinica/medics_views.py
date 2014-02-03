#!/usr/bin/env python
# -*- coding: utf-8 *-*


from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth #para login
from django.contrib.auth.models import User


from HistoriaClinica.models import *
import HistoriaClinica.forms as my_forms
from utils import *
from globals import *
from HTMLTags import *

from verbose import *


## Imagenes

def medic_add_patients_images(request, pac_username):
    """
        Muestra el listado de imagenes subidas de los diferentes examenenes
        realizados al paciente
    """
    mi_template = get_template('Medics/HistoriaClinica/agregar-imagen.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac
        #dict['show_form'] = True
        dict['show_errors'] = False

        if request.method == 'POST':
            form = my_forms.ImageForm(request.POST, request.FILES)
            if form.is_valid():
                img = Image(
                    medic = request.user,
                    patient = pac,
                    title = form.cleaned_data['title'],
                    content = form.cleaned_data['content'],
                    image = form.cleaned_data['image'],
                )
                img.save()
                dict['custom_message'] = html_message('Imagen Subida con Exito', 'success')
                form = my_forms.ImageForm()
                dict['form'] = form
            else:
                dict['show_errors'] = True
                dict['form'] = form

        else:
            form = my_forms.ImageForm()
            dict['form'] = form

    #usuario no posee permisos
    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_list_patients_images(request, pac_username):
    """
        Muestra el listado de imagenes subidas de los diferentes examenenes
        realizados al paciente
    """
    mi_template = get_template('Medics/HistoriaClinica/mostrar-imagenes.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        dict['pac'] = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['images'] = Image.objects.filter(patient__username=pac_username)

    #usuario no posee permisos
    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_show_patients_images(request, pac_username):
    """
        Muestra el listado de imagenes subidas de los diferentes examenenes
        realizados al paciente
    """
    mi_template = get_template('Medics/HistoriaClinica/mostrar-imagenes.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        dict['pac'] = User.objects.get(groups__name='Paciente', username=pac_username)


    #usuario no posee permisos
    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)


def medic_edit_patient_image(request, img_id):
    mi_template = get_template('Medics/HistoriaClinica/modificar-image-info.html')
    dict = generate_base_keys(request)
    dict['show_errors'] = False
    dict['show_form'] = True

    if request.user.is_authenticated():
        image = Image.objects.get(id=img_id)
        dict['pac_username'] = image.patient.username
        pac = image.patient
        dict['pac'] = pac
        dict['img'] = image
        form_data = {
            'title' : image.title,
            'content' : image.content
        }

        if request.method == 'POST':
            form = my_forms.ImageInfoForm(request.POST)

            if form.is_valid() :
                #image = Image.objects.get(id=img_id)
                image.title =  form.cleaned_data['title']
                image.content =  form.cleaned_data['content']
                image.save()

                return HttpResponseRedirect("/pacientes/mostrar/imagenes/%s/" %image.patient.username)
            else:
                dict['show_errors'] = True
                dict['form'] = form

        else:
            dict['form'] = my_forms.ImageInfoForm(initial=form_data)


        html_cont = mi_template.render(Context(dict))
        return HttpResponse(html_cont)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)



def medic_del_patient_image(request, img_id):
    #incomplete
    mi_template = get_template('Medics/HistoriaClinica/borrar-imagen.html')
    dict = generate_base_keys(request)

    if True:
        try:
            exam = Image.objects.get(id=img_id)
            dict['exam'] = exam
            dict['exam_lbl'] = get_labels_for(exam)
            dict['pac'] = exam.patient
            dict['pac_username'] = exam.patient.username

            dict['exam_name'] = exam.title
            dict['return_url'] = "/pacientes/mostrar/imagenes/%s/" %dict['pac_username']

            if request.method == 'POST':
                Image.objects.get(id=img_id).delete()
                dict['response'] = True

            else:
                dict['answer'] = True

        except:
            path = request.META['PATH_INFO']
            return HttpResponseRedirect("/restricted-access%s" %path)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)


## Antecedentes Perinatales


def medic_view_patient_perinatal_antecedents(request, pac_username):
    """
        Muestra los antecedentes perinatales del paciente

        Argv:
            pac_username: n
    """
    mi_template = get_template('Medics/HistoriaClinica/mostrar-antecedentes-perinatales.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac
        try:
            antp = AntecedentesPerinatales.objects.get(patient=pac)

        #si no posee se crea uno vacio o nulo
        except AntecedentesPerinatales.DoesNotExist:
            antp = AntecedentesPerinatales.objects.create(
                patient = pac,
                pregnancy_number = 0,
                pregnancy_duration = 0,
                controls = '-',
                normal_birth = '-',
                weight = 0,
                size = 0,
                pathologies = '-',
                medical_care = '-',
                coments = "Antecedentes Perinatales no Definidos"
            )
            antp.save()
        dict['antp'] = antp

    #usuario no posee permisos
    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_edit_patient_perinatal_antecedents(request, pac_username):
    """

    """
    mi_template = get_template('Medics/HistoriaClinica/modificar-antecedentes-perinatales.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac

        antp = AntecedentesPerinatales.objects.get(patient=pac)

        if request.method == 'POST':
            form = my_forms.AntecedentesPerinatalesForm(request.POST)
            if form.is_valid():
                antp.pregnancy_number = form.cleaned_data['pregnancy_number']
                antp.pregnancy_duration = form.cleaned_data['pregnancy_duration']
                antp.controls = form.cleaned_data['controls'];
                antp.normal_birth = form.cleaned_data['normal_birth']
                antp.weight = form.cleaned_data['weight']
                antp.size = form.cleaned_data['size']
                antp.pathologies = form.cleaned_data['pathologies']
                antp.medical_care = form.cleaned_data['medical_care']
                antp.coments = form.cleaned_data['coments']
                antp.save()
                dict['custom_message'] = html_message('Datos Actualizados Correctamente', 'success')

            else:
                dict['show_errors'] = True
                dict['form'] = form

        else:
            form = my_forms.AntecedentesPerinatalesForm(instance=antp)
            dict['form'] = form

        #incompleto

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)


## Habitos Toxicos

def medic_view_patient_toxic_habits(request, pac_username):
    """
    Mostrar Habitos Toxicos
    """
    mi_template = get_template('Medics/HistoriaClinica/mostrar-habitos-toxicos.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac

        try:
            habt = ToxicHabits.objects.get(patient=pac)
        #si no posee se crea uno vacio o nulo
        except ToxicHabits.DoesNotExist:
            habt = ToxicHabits.objects.create(
                patient = pac,
                snuff = '-',
                alcohol = '-',
                drugs = '-',
                infusions = '-',
                observations = 'No hay datos',
            )
            habt.save()
        dict['habt'] = habt

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_edit_patient_toxic_habits(request, pac_username):
    """
        Modificar la informacion sobre los habitos toxicos del paciente
    """
    mi_template = get_template('Medics/HistoriaClinica/modificar-habitos-toxicos.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac

        habt = ToxicHabits.objects.get(patient=pac)

        if request.method == 'POST':
            form = my_forms.ToxicHabitsForm(request.POST)
            if form.is_valid():
                habt.snuff = form.cleaned_data['snuff']
                habt.alcohol = form.cleaned_data['alcohol']
                habt.drugs = form.cleaned_data['drugs']
                habt.infusions = form.cleaned_data['infusions']
                habt.observations = form.cleaned_data['observations']
                habt.save()
                dict['custom_message'] = html_message('Datos Actualizados Correctamente', 'success')

            else:
                dict['show_errors'] = True
                dict['form'] = form

        else:
            form = my_forms.ToxicHabitsForm(instance=habt)
            dict['form'] = form

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)

# Examenes Fisico

def medic_list_patient_phisic_exam(request, pac_username):
    mi_template = get_template('Medics/HistoriaClinica/listado-examen-fisico.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac
        dict['BasicExams'] = BasicExam.objects.filter(patient=pac)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_show_patient_phisic_exam(request, exam_id):

    mi_template = get_template('Medics/HistoriaClinica/mostrar-examen-fisico.html')
    dict = generate_base_keys(request)

    if True:
        exam = BasicExam.objects.get(id=exam_id)
        dict['exam'] = exam
        dict['exam_lbl'] = get_labels_for(exam)
        dict['pac'] = exam.patient
        dict['pac_username'] = exam.patient.username

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_add_patient_phisic_exam(request, pac_username):
    """
     Agregar un examen Basico
    """
    mi_template = get_template('Medics/HistoriaClinica/nuevo-examen-fisico.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac

        form = my_forms.BasicExamForm(auto_id=False)
        dict['show_errors'] = False
        dict['show_form'] = True

        if request.method == 'POST':
            form = my_forms.BasicExamForm(request.POST, auto_id=False)
            if form.is_valid():
                b_exam = BasicExam(
                    patient = pac,
                    body_temperature = form.cleaned_data['body_temperature'],
                    sistolic_blood_pressure  = form.cleaned_data['sistolic_blood_pressure'],
                    diastolic_blood_pressure = form.cleaned_data['diastolic_blood_pressure'],
                    respiratory_rate = form.cleaned_data['respiratory_rate'],
                    pulse = form.cleaned_data['sistolic_blood_pressure'] - form.cleaned_data['diastolic_blood_pressure'],
                    average_weight = form.cleaned_data['average_weight'],
                    average_height = form.cleaned_data['average_height'],
                    weight = form.cleaned_data['weight'],
                    height = form.cleaned_data['height'],
                    #size = form.cleaned_data['size'],
                    bmi = form.cleaned_data['bmi'],
                    general_impression = form.cleaned_data['general_impression'],
                )
                b_exam.save()
                dict['show_form'] = False
                dict['custom_message'] = html_message('Examen Registrado Correctamente', 'success')

            else: #errores campos
                dict['show_errors'] = True
                dict['form'] = form

        else:
            dict['form'] = form

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)


#don't implement
#def medic_edit_patient_phisic_exam(request, pac_username):
    ##incomplete
    #mi_template = get_template('Medics/HistoriaClinica/listado-examen-fisico.html')
    #dict = generate_base_keys(request)

    #if True:
        #dict['pac_username'] = pac_username
        #pac = User.objects.get(groups__name='Paciente', username=pac_username)
        #dict['pac'] = pac

        ##incompleto

    #else:
        #path = request.META['PATH_INFO']
        #return HttpResponseRedirect("/restricted-access%s" %path)

    #html_cont = mi_template.render(Context(dict))
    #return HttpResponse(html_cont)


def medic_del_patient_phisic_exam(request, exam_id):
    #incomplete
    mi_template = get_template('Medics/HistoriaClinica/borrar-examen.html')
    dict = generate_base_keys(request)

    if True:
        try:
            exam = BasicExam.objects.get(id=exam_id)

            dict['exam'] = exam
            dict['exam_lbl'] = get_labels_for(exam)
            dict['pac'] = exam.patient
            dict['pac_username'] = exam.patient.username

            dict['exam_name'] = "Fisico"
            dict['return_url'] = "/pacientes/listado/examen-fisico/%s/" %dict['pac_username']

            if request.method == 'POST':
                BasicExam.objects.get(id=exam_id).delete()
                dict['response'] = True

            else:
                dict['answer'] = True

        except:
            path = request.META['PATH_INFO']
            return HttpResponseRedirect("/restricted-access%s" %path)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)


## Examenes de Cabeza


def medic_list_patient_head_exam(request, pac_username):
    mi_template = get_template('Medics/HistoriaClinica/listado-examen-cabeza.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac
        dict['HeadExams'] = HeadExam.objects.filter(patient=pac)
        #incompleto

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_add_patient_head_exam(request, pac_username):
    mi_template = get_template('Medics/HistoriaClinica/agregar-examen-cabeza.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac
        #_form = my_forms.HeadExamForm(auto_id=False)
        dict['show_errors'] = False
        dict['show_form'] = True

        if request.method == 'POST':
            _form = my_forms.HeadExamForm(request.POST, auto_id=False)
            if _form.is_valid():
                exam = HeadExam(
                    patient = pac,

                    form = _form.cleaned_data['form'],
                    scalp = _form.cleaned_data['scalp'],
                    skull = _form.cleaned_data['skull'],
                    fontanelles_and_sutures = _form.cleaned_data['fontanelles_and_sutures'],
                    facie = _form.cleaned_data['facie'],
                    eyelids = _form.cleaned_data['eyelids'],
                    conjunctive = _form.cleaned_data['conjunctive'],
                    eyeball_movement = _form.cleaned_data['eyeball_movement'],
                    vision = _form.cleaned_data['vision'],
                    vision_p1 = _form.cleaned_data['vision_p1'],
                    vision_p2 = _form.cleaned_data['vision_p2'],
                    vision_p3 = _form.cleaned_data['vision_p3'],
                    nose = _form.cleaned_data['nose'],
                    nostril = _form.cleaned_data['nostril'],
                    lips = _form.cleaned_data['lips'],
                    teeth = _form.cleaned_data['teeth'],
                    language = _form.cleaned_data['language'],
                    oropharyngeal_mucosa = _form.cleaned_data['oropharyngeal_mucosa'],
                    tonsils = _form.cleaned_data['tonsils'],
                    ears = _form.cleaned_data['ears'],
                    ear_canal = _form.cleaned_data['ear_canal'],
                    eardrums = _form.cleaned_data['eardrums'],
                    hearing = _form.cleaned_data['hearing'],
                    observations = _form.cleaned_data['observations']
                )
                exam.save()
                dict['show_form'] = False
                dict['custom_message'] = html_message('Examen Registrado Correctamente', 'success')

            else:
                dict['show_errors'] = True
        else:
            _form = my_forms.HeadExamForm(auto_id=False)
        dict['form'] = _form

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_show_patient_head_exam(request, exam_id):

    mi_template = get_template('Medics/HistoriaClinica/mostrar-examen-cabeza.html')
    dict = generate_base_keys(request)

    if True:
        exam = HeadExam.objects.get(id=exam_id)
        dict['exam'] = exam
        dict['exam_lbl'] = get_labels_for(exam)
        dict['pac'] = exam.patient
        dict['pac_username'] = exam.patient.username

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)


def medic_del_patient_head_exam(request, exam_id):
    #incomplete
    mi_template = get_template('Medics/HistoriaClinica/borrar-examen.html')
    dict = generate_base_keys(request)

    if True:
        try:
            exam = HeadExam.objects.get(id=exam_id)
            dict['exam'] = exam
            dict['exam_lbl'] = get_labels_for(exam)
            dict['pac'] = exam.patient
            dict['pac_username'] = exam.patient.username

            dict['exam_name'] = "de Cabeza"
            dict['return_url'] = "/pacientes/listado/examen-cabeza/%s/" %dict['pac_username']

            if request.method == 'POST':
                BasicExam.objects.get(id=exam_id).delete()
                dict['response'] = True

            else:
                dict['answer'] = True

        except:
            path = request.META['PATH_INFO']
            return HttpResponseRedirect("/restricted-access%s" %path)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)


#def medic_add_patient_prescription(request, patient):
    #mi_template = get_template('Medics/GestionTurnos/agregar-receta-medica.html')
    #dict = generate_base_keys(request)

    #if True:
        #pass

    #else:
        #path = request.META['PATH_INFO']
        #return HttpResponseRedirect("/restricted-access%s" %path)

    #html_cont = mi_template.render(Context(dict))
    #return HttpResponse(html_cont)


## examen cuello

def medic_add_patient_neck_exam(request, pac_username):
    mi_template = get_template('Medics/HistoriaClinica/agregar-examen-cuello.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac
        #_form = my_forms.HeadExamForm(auto_id=False)
        dict['show_errors'] = False
        dict['show_form'] = True

        if request.method == 'POST':
            _form = my_forms.NeckExamForm(request.POST, auto_id=False)
            if _form.is_valid():
                exam = NeckExam(
                    patient = pac,
                    inspection = _form.cleaned_data['inspection'],
                    palpation = _form.cleaned_data['palpation'],
                    percussion = _form.cleaned_data['percussion'],
                    auscultation = _form.cleaned_data['auscultation'],
                    comments = _form.cleaned_data['comments']
                )
                exam.save()
                dict['show_form'] = False
                dict['custom_message'] = html_message('Examen Registrado Correctamente', 'success')

            else:
                dict['show_errors'] = True
        else:
            _form = my_forms.NeckExamForm(auto_id=False)
            dict['form'] = _form

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_list_patient_neck_exam(request, pac_username):
    mi_template = get_template('Medics/HistoriaClinica/listado-examen-cuello.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac
        dict['NeckExams'] = NeckExam.objects.filter(patient=pac)


    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_show_patient_neck_exam(request, exam_id):

    mi_template = get_template('Medics/HistoriaClinica/mostrar-examen-cuello.html')
    dict = generate_base_keys(request)

    if True:
        exam = NeckExam.objects.get(id=exam_id)
        dict['exam'] = exam
        dict['exam_lbl'] = get_labels_for(exam)
        dict['pac'] = exam.patient
        dict['pac_username'] = exam.patient.username

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_del_patient_neck_exam(request, exam_id):
    #incomplete
    mi_template = get_template('Medics/HistoriaClinica/borrar-examen.html')
    dict = generate_base_keys(request)

    if True:
        try:
            exam = NeckExam.objects.get(id=exam_id)
            dict['exam'] = exam
            dict['exam_lbl'] = get_labels_for(exam)
            dict['pac'] = exam.patient
            dict['pac_username'] = exam.patient.username

            dict['exam_name'] = "de Cuello"
            dict['return_url'] = "/pacientes/listado/examen-cuello/%s/" %dict['pac_username']

            if request.method == 'POST':
                NeckExam.objects.get(id=exam_id).delete()
                dict['response'] = True

            else:
                dict['answer'] = True

        except:
            path = request.META['PATH_INFO']
            return HttpResponseRedirect("/restricted-access%s" %path)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)

## piel faneas tejidos subcutaneo



def medic_add_patient_pfts_exam(request, pac_username):
    mi_template = get_template('Medics/HistoriaClinica/agregar-examen-piel.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac
        #_form = my_forms.HeadExamForm(auto_id=False)
        dict['show_errors'] = False
        dict['show_form'] = True

        if request.method == 'POST':
            _form = my_forms.PFTSExamForm(request.POST, auto_id=False)
            if _form.is_valid():
                exam = PFTSExam(
                    patient = pac,
                    aspect = _form.cleaned_data['aspect'],
                    pilosa_distribution = _form.cleaned_data['pilosa_distribution'],
                    injuries = _form.cleaned_data['injuries'],
                    appendages = _form.cleaned_data['appendages'],
                    subcutaneous_tissue = _form.cleaned_data['subcutaneous_tissue'],
                )
                exam.save()
                dict['show_form'] = False
                dict['custom_message'] = html_message('Examen Registrado Correctamente', 'success')

            else:
                dict['show_errors'] = True
        else:
            _form = my_forms.PFTSExamForm(auto_id=False)
            dict['form'] = _form

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_list_patient_pfts_exam(request, pac_username):
    mi_template = get_template('Medics/HistoriaClinica/listado-examen-piel.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac
        dict['PFTSExams'] = PFTSExam.objects.filter(patient=pac)


    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_show_patient_pfts_exam(request, exam_id):

    mi_template = get_template('Medics/HistoriaClinica/mostrar-examen-piel.html')
    dict = generate_base_keys(request)

    if True:
        exam = PFTSExam.objects.get(id=exam_id)
        dict['exam'] = exam
        dict['exam_lbl'] = get_labels_for(exam)
        dict['pac'] = exam.patient
        dict['pac_username'] = exam.patient.username

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_del_patient_pfts_exam(request, exam_id):
    #incomplete
    mi_template = get_template('Medics/HistoriaClinica/borrar-examen.html')
    dict = generate_base_keys(request)

    if True:
        try:
            exam = PFTSExam.objects.get(id=exam_id)
            dict['exam'] = exam
            dict['exam_lbl'] = get_labels_for(exam)
            dict['pac'] = exam.patient
            dict['pac_username'] = exam.patient.username

            dict['exam_name'] = "de Cabeza"
            dict['return_url'] = "/pacientes/listado/examen-piel-faneras/%s/" %dict['pac_username']

            if request.method == 'POST':
                PFTSExam.objects.get(id=exam_id).delete()
                dict['response'] = True

            else:
                dict['answer'] = True

        except:
            path = request.META['PATH_INFO']
            return HttpResponseRedirect("/restricted-access%s" %path)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)


## Examen Osteo Articular


def medic_add_patient_osteo_art_exam(request, pac_username):
    mi_template = get_template('Medics/HistoriaClinica/agregar-examen-osteo-articular.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac
        #_form = my_forms.HeadExamForm(auto_id=False)
        dict['show_errors'] = False
        dict['show_form'] = True

        if request.method == 'POST':
            _form = my_forms.OsteoArticularExamForm(request.POST, auto_id=False)
            if _form.is_valid():
                exam = OsteoArticularExam(
                    patient = pac,
                    vertebra_column = _form.cleaned_data['vertebra_column'],
                    bone_axles =  _form.cleaned_data['bone_axles'],
                    joints =  _form.cleaned_data['joints'],
                    members =  _form.cleaned_data['members'],
                    muscular_tropism =  _form.cleaned_data['muscular_tropism']
                )
                exam.save()
                dict['show_form'] = False
                dict['custom_message'] = html_message('Examen Registrado Correctamente', 'success')

            else:
                dict['show_errors'] = True
        else:
            _form = my_forms.OsteoArticularExamForm(auto_id=False)
            dict['form'] = _form

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_list_patient_osteo_art_exam(request, pac_username):
    mi_template = get_template('Medics/HistoriaClinica/listado-examen-osteo-articular.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac
        dict['OsteoArtExams'] = OsteoArticularExam.objects.filter(patient=pac)


    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_show_patient_osteo_art_exam(request, exam_id):

    mi_template = get_template('Medics/HistoriaClinica/mostrar-examen-osteo-articular.html')
    dict = generate_base_keys(request)

    if True:
        exam = OsteoArticularExam.objects.get(id=exam_id)
        dict['exam'] = exam
        dict['exam_lbl'] = get_labels_for(exam)
        dict['pac'] = exam.patient
        dict['pac_username'] = exam.patient.username

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_del_patient_osteo_art_exam(request, exam_id):
    #incomplete
    mi_template = get_template('Medics/HistoriaClinica/borrar-examen.html')
    dict = generate_base_keys(request)

    if True:
        try:
            exam = OsteoArticularExam.objects.get(id=exam_id)
            dict['exam'] = exam
            dict['exam_lbl'] = get_labels_for(exam)
            dict['pac'] = exam.patient
            dict['pac_username'] = exam.patient.username

            dict['exam_name'] = "Osteo Articular"
            dict['return_url'] = "/pacientes/listado/examen-osteo-articular/%s/" %dict['pac_username']

            if request.method == 'POST':
                OsteoArticularExam.objects.get(id=exam_id).delete()
                dict['response'] = True

            else:
                dict['answer'] = True

        except:
            path = request.META['PATH_INFO']
            return HttpResponseRedirect("/restricted-access%s" %path)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



#Examen Torax y Aparato Respiratorio

def medic_add_patient_resp_system_exam(request, pac_username):
    mi_template = get_template('Medics/HistoriaClinica/agregar-examen-respiratorio.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac
        #_form = my_forms.HeadExamForm(auto_id=False)
        dict['show_errors'] = False
        dict['show_form'] = True

        if request.method == 'POST':
            _form = my_forms.RespiratorySystemExamForm(request.POST, auto_id=False)
            if _form.is_valid():
                exam = RespiratorySystemExam(
                    patient = pac,
                    type_chest = _form.cleaned_data['type_chest'],
                    breast = _form.cleaned_data['breast'],
                    accessory_muscle_use = _form.cleaned_data['accessory_muscle_use'],
                    respiratory_rate = _form.cleaned_data['respiratory_rate'],
                    tour_freely = _form.cleaned_data['tour_freely'],
                    tour_vertices = _form.cleaned_data['tour_vertices'],
                    jars_vibrations = _form.cleaned_data['jars_vibrations'],
                    sonority = _form.cleaned_data['sonority'],
                    vesicular_murmur = _form.cleaned_data['vesicular_murmur'],
                    rales_moist_rales = _form.cleaned_data['rales_moist_rales'],
                    roncus = _form.cleaned_data['roncus'],
                    wheezing = _form.cleaned_data['wheezing'],
                    tubal_puff = _form.cleaned_data['tubal_puff'],
                    pleural_rub = _form.cleaned_data['pleural_rub'],
                    comments = _form.cleaned_data['comments']
                )
                exam.save()
                dict['show_form'] = False
                dict['custom_message'] = html_message('Examen Registrado Correctamente', 'success')

            else:
                dict['show_errors'] = True
        else:
            _form = my_forms.RespiratorySystemExamForm(auto_id=False)
            dict['form'] = _form

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_list_patient_resp_system_exam(request, pac_username):
    mi_template = get_template('Medics/HistoriaClinica/listado-examen-respiratorio.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac
        dict['RespExams'] = RespiratorySystemExam.objects.filter(patient=pac)


    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_show_patient_resp_system_exam(request, exam_id):

    mi_template = get_template('Medics/HistoriaClinica/mostrar-examen-respiratorio.html')
    dict = generate_base_keys(request)

    if True:
        exam = RespiratorySystemExam.objects.get(id=exam_id)
        dict['exam'] = exam
        dict['exam_lbl'] = get_labels_for(exam)
        dict['pac'] = exam.patient
        dict['pac_username'] = exam.patient.username

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_del_patient_resp_system_exam(request, exam_id):
    #incomplete
    mi_template = get_template('Medics/HistoriaClinica/borrar-examen.html')
    dict = generate_base_keys(request)

    if True:
        try:
            exam = RespiratorySystemExam.objects.get(id=exam_id)
            dict['exam'] = exam
            dict['exam_lbl'] = get_labels_for(exam)
            dict['pac'] = exam.patient
            dict['pac_username'] = exam.patient.username

            dict['exam_name'] = "Torax y Aparato Respiratorio"
            dict['return_url'] = "/pacientes/listado/examen-aparato-respiratorio/%s/" %dict['pac_username']

            if request.method == 'POST':
                RespiratorySystemExam.objects.get(id=exam_id).delete()
                dict['response'] = True

            else:
                dict['answer'] = True

        except:
            path = request.META['PATH_INFO']
            return HttpResponseRedirect("/restricted-access%s" %path)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)


## Examen Aparato Cardiovascular (incompleto)

def medic_add_patient_cardio_exam(request, pac_username):
    mi_template = get_template('Medics/HistoriaClinica/agregar-examen-cardio.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac
        #_form = my_forms.HeadExamForm(auto_id=False)
        dict['show_errors'] = False
        dict['show_form'] = True

        if request.method == 'POST':
            _form = my_forms.CardiovascularSystemExamForm(request.POST, auto_id=False)
            if _form.is_valid():
                exam = CardiovascularSystemExam(
                    patient = pac,
                    beats = _form.cleaned_data['beats'],
                    shock_tip = _form.cleaned_data['shock_tip'],
                    R1 = _form.cleaned_data['R1'],
                    R2 = _form.cleaned_data['R2'],
                    R3 = _form.cleaned_data['R3'],
                    R4 = _form.cleaned_data['R4'],
                    puffs = _form.cleaned_data['puffs'],
                    clicks = _form.cleaned_data['clicks'],
                    carotid_pulse = _form.cleaned_data['carotid_pulse'],
                    humeral_pulse = _form.cleaned_data['humeral_pulse'],
                    radial_pulse = _form.cleaned_data['radial_pulse'],
                    femoral_pulse = _form.cleaned_data['femoral_pulse'],
                    popliteal_pulse = _form.cleaned_data['popliteal_pulse'],
                    posterior_tibial_pulse = _form.cleaned_data['posterior_tibial_pulse'],
                    pedius_pulse = _form.cleaned_data['pedius_pulse'],
                    comments = _form.cleaned_data['comments'],
                )
                exam.save()
                dict['show_form'] = False
                dict['custom_message'] = html_message('Examen Registrado Correctamente', 'success')

            else:
                dict['form'] = _form
                dict['show_errors'] = True
        else:
            _form = my_forms.CardiovascularSystemExamForm(auto_id=False)
            dict['form'] = _form

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_list_patient_cardio_exam(request, pac_username):
    mi_template = get_template('Medics/HistoriaClinica/listado-examen-cardio.html')
    dict = generate_base_keys(request)

    if True:
        dict['pac_username'] = pac_username
        pac = User.objects.get(groups__name='Paciente', username=pac_username)
        dict['pac'] = pac
        dict['CardioExams'] = CardiovascularSystemExam.objects.filter(patient=pac)


    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_show_patient_cardio_exam(request, exam_id):

    mi_template = get_template('Medics/HistoriaClinica/mostrar-examen-cardio.html')
    dict = generate_base_keys(request)

    if True:
        exam =  CardiovascularSystemExam.objects.get(id=exam_id)
        dict['exam'] = exam
        dict['exam_lbl'] = get_labels_for(exam)
        dict['pac'] = exam.patient
        dict['pac_username'] = exam.patient.username

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def medic_del_patient_cardio_exam(request, exam_id):
    #incomplete
    mi_template = get_template('Medics/HistoriaClinica/borrar-examen.html')
    dict = generate_base_keys(request)

    if True:
        try:
            exam = CardiovascularSystemExam.objects.get(id=exam_id)
            dict['exam'] = exam
            dict['exam_lbl'] = get_labels_for(exam)
            dict['pac'] = exam.patient
            dict['pac_username'] = exam.patient.username

            dict['exam_name'] = "Aparato Cardiovascular"
            dict['return_url'] = "/pacientes/listado/examen-aparato-cardiovascular/%s/" %dict['pac_username']

            if request.method == 'POST':
                CardiovascularSystemExam.objects.get(id=exam_id).delete()
                dict['response'] = True

            else:
                dict['answer'] = True

        except:
            path = request.META['PATH_INFO']
            return HttpResponseRedirect("/restricted-access%s" %path)

    else:
        path = request.META['PATH_INFO']
        return HttpResponseRedirect("/restricted-access%s" %path)

    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)