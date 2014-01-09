#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User

import datetime
from globals import *
from utils import date_to_str



class Image(models.Model):
    """
    Imagenes Subidas
    """
    date = models.DateField("Fecha", auto_now_add=True)
    medic = models.ForeignKey(User, related_name='medic_user0')
    patient = models.ForeignKey(User, related_name='patient_user0')
    title = models.CharField("Titulo", max_length=125, default='')
    content = models.TextField("Contenido", default='')
    image = models.ImageField("Imagen", upload_to='upload/images')


    class Meta:
        db_table = "Images"



class File(models.Model):
    """
    Archivos Subidos
    """
    date = models.DateField(auto_now_add=True)
    medic = models.ForeignKey(User, related_name='medic_user1')
    patient = models.ForeignKey(User, related_name='patient_user1')
    title = models.CharField(max_length=125, default='')
    content = models.TextField(default='')
    archive = models.FileField(upload_to='upload/files')


    class Meta:
        db_table = "Files"


    def get_file_ext(self):
        """
            Obtiene la extencion o terminacion del archivo, no distingue
            el bite code interno
            doc, pdf, xls, txt, etc..
        """
        return self.archive.url.split('.')[-1].lower()



class AntecedentesPerinatales(models.Model):
    """
        Referentes al nacimiento
    """
    patient = models.ForeignKey(User,  unique=True) #fk
    pregnancy_number = models.IntegerField('Embarazo Nro')
    pregnancy_duration = models.IntegerField('Duracion/Semanas') #en semanas
    controls = models.CharField('Controles Durante Embarazo', max_length=1, choices=TRUE_FALSE_CHOICE) #si tubo controles durante el embarazo
    normal_birth = models.CharField('Parto Normal', max_length=1, choices=TRUE_FALSE_CHOICE) #si nacio parto normal o cesareas
    weight = models.FloatField('Peso al Nacer') #peso al nacer
    size = models.FloatField('Talla') #talla
    pathologies = models.CharField('Presento Patologias al Nacer', max_length=1, choices=TRUE_FALSE_CHOICE) #al nacer S/N
    medical_care = models.CharField('Requirio Atencion Medica', max_length=1, choices=TRUE_FALSE_CHOICE)# requirio atencion medica S/N
    coments = models.TextField('Otros Datos de Relevancia o Informacion Adicional') #otra informacion relevante

    class Meta:
        db_table = "AntecedentesPerinatales"



class ToxicHabits(models.Model):
    """
        Habitos toxicos del paciente
    """
    patient = models.ForeignKey(User,  unique=True) #fk
    snuff = models.CharField('Tabaco', max_length=1,  choices=TRUE_FALSE_CHOICE)
    alcohol = models.CharField('Alcohol', max_length=1,  choices=TRUE_FALSE_CHOICE)
    drugs = models.CharField('Drogas', max_length=1,  choices=TRUE_FALSE_CHOICE)
    infusions = models.CharField('Infuciones', max_length=1, choices=TRUE_FALSE_CHOICE)
    observations = models.TextField('Observaciones')

    class Meta:
        db_table = "HabitosToxicos"



class BasicExam(models.Model):
    """
    Examen Base
    """
    patient = models.ForeignKey(User) #fk
    date = models.DateField("Fecha del Examen", auto_now_add=True)

    #signos vitales
    body_temperature = models.FloatField("Temperatura Corporal")
    sistolic_blood_pressure = models.IntegerField("Presion Arterial Sistolica")
    diastolic_blood_pressure = models.IntegerField("Presion Arterial Dastolica")
    respiratory_rate = models.IntegerField("Frecuencia Respiratoria")
    pulse = models.IntegerField("Pulso")

    average_weight = models.FloatField("Peso Promedio")
    average_height = models.FloatField("Altura Promedio")
    weight = models.FloatField("Peso")
    height = models.FloatField("Altura")
    #size = models.CharField("Talla", max_length=30)
    bmi = models.FloatField("Indice de Masa Corporal") #indice de masa corporal
    general_impression = models.TextField("Imprecion General") #text


    class Meta:
        db_table = "ExamenesBase"


    #calculado segun info obtenida en la siguiente presentacion
    #http://www.slideshare.net/lSpical/5examen-fisico-signos-vitales-y-apreciacion-general
    def presion_art_pulso(self):
        """
        """
        return self.sistolic_blood_pressure - self.diastolic_blood_pressure


    def overweight(self):
        """
        Exceso de peso
        """
        return self.weight - self.average_weight


    def overweight_lbl(self):
        return self.overweight.__doc__


    def calc_pulse(self):
        """
        """
        self.pulse = self.presion_art_pulso()


    def presion_art_media(self):
        """
        """
        return self.diastolic_blood_pressure + (self.pres_art_pulso() / 3)


    def _date(self):
        """
        """
        return self.date.strftime('%d/%m/%Y')


    def __str__(self):
        return "Examen Realizado el: %s" %self.date.strftime('%d/%m/%Y')




class HeadExam(models.Model):
    patient = models.ForeignKey(User) #fk
    date = models.DateField("Fecha del Examen", auto_now_add=True)

    form = models.CharField('Forma', max_length=128)
    scalp = models.CharField('Cuero Cabelludo', max_length=128)
    skull = models.CharField('Craneo', max_length=128)  #N/A Normal - Alterado
    fontanelles_and_sutures = models.CharField('Fontanelas y Suturas', max_length=1, default='-', choices=ESTADO_CHOICE)  #N/A Normal - Alterado
    facie = models.CharField(max_length=1, default='-', choices=ESTADO_CHOICE)  #N/A Normal - Alterado
    eyelids = models.CharField('Parpados', max_length=1, default='-', choices=ESTADO_CHOICE)  #N/A Normal - Alterado
    conjunctive = models.CharField('Conjuntivas', max_length=1, default='-', choices=ESTADO_CHOICE)  #N/A Normal - Alterado
    eyeball_movement = models.CharField('Movimiento Globo Ocular', max_length=1, default='-', choices=ESTADO_CHOICE)  #N/A Normal - Alterado
    vision = models.CharField('Vista', max_length=1, default='-', choices=ESTADO_CHOICE)  #N/A Normal - Alterado
    vision_p1 = models.CharField('Vista Problema', max_length=1, default='-', choices=VISION_CHOICE)
    vision_p2 = models.CharField('Vista Problema', max_length=1, default='-', choices=VISION_CHOICE)
    vision_p3 = models.CharField('Vista Problema', max_length=1, default='-', choices=VISION_CHOICE)
    nose = models.CharField('Nariz', max_length=1, default='-', choices=NOSE_CHOICE)
    nostril = models.CharField('Fosas Nasales', max_length=1, default='-', choices=ESTADO_CHOICE)  #N/A Normal - Alterado
    lips = models.CharField('Labios' ,max_length=1, default='N', choices=LIPS_CHOICE)
    teeth = models.CharField('Dientes', max_length=1, default='-', choices=ESTADO_CHOICE)  #N/A Normal - Alterado
    language = models.CharField('Lengua', max_length=1, default='-', choices=ESTADO_CHOICE)  #N/A Normal - Alterado
    oropharyngeal_mucosa = models.CharField('Mucosa Bucofaringea', max_length=1, default='-', choices=ESTADO_CHOICE)  #N/A Normal - Alterado
    tonsils = models.CharField('Agmidalas' ,max_length=1, default='-', choices=ESTADO_CHOICE)  #N/A Normal - Alterado
    ears = models.CharField('Pabellones Auriculares' ,max_length=1, default='-', choices=ESTADO_CHOICE)  #N/A Normal - Alterado
    ear_canal = models.CharField('Conducto Auditivo Externo',max_length=1, default='-', choices=ESTADO_CHOICE)  #N/A Normal - Alterado
    eardrums = models.CharField('Timpanos', max_length=1, default='-', choices=ESTADO_CHOICE)  #N/A Normal - Alterado
    hearing = models.CharField('Problemas Audicion', max_length=1, default='N', choices=HEARING_CHOICE)  #N/A Normal - Alterado
    observations = models.TextField('Observaciones')


    class Meta:
        db_table = "ExamenesCabeza"


