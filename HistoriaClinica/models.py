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



class NeckExam(models.Model):
    """
    Examen de Cuello
    """
    patient = models.ForeignKey(User) #fk
    date = models.DateField("Fecha del Examen", auto_now_add=True)

    inspection = models.CharField('Inspecion', max_length=250)
    palpation = models.CharField('Palpacion', max_length=250)
    percussion = models.CharField('Percusion', max_length=250)
    auscultation = models.CharField('Ausculacion', max_length=250)
    comments = models.TextField('Observaciones')


    class Meta:
        db_table = "ExamenesCuello"




class PFTSExam(models.Model):
    """
        Examen Fisico - Analisis de Piel, Faneas y Tejido Subcutaneo
    """
    patient = models.ForeignKey(User) #fk
    date = models.DateField("Fecha del Examen", auto_now_add=True)

    aspect = models.TextField('Aspecto')
    pilosa_distribution = models.TextField('Distribucion Pilosa')
    injuries = models.TextField('Leciones')
    appendages = models.TextField('Faneras')
    subcutaneous_tissue = models.TextField('Tejido Celular Subcutaneo')


    class Meta:
        db_table = "ExamenesPielFaneasTejSubCutaneo"



class OsteoArticularExam(models.Model):
    patient = models.ForeignKey(User) #fk
    date = models.DateField("Fecha del Examen", auto_now_add=True)

    vertebra_column = models.TextField('Columna Vertebral')
    bone_axles = models.TextField('Ejes Oseos')
    joints = models.TextField('Articulaciones')
    members = models.TextField('Miembros')
    muscular_tropism = models.TextField('Trofismo muscular')



class RespiratorySystemExam(models.Model):
    """
        Examen Torax y Aparato respiratorio
    """
    patient = models.ForeignKey(User) #fk
    date = models.DateField("Fecha del Examen", auto_now_add=True)

    type_chest = models.CharField('Tipo de Torax', max_length=1, default='N', choices=TYPE_THORAX_CHOICE)
    breast = models.TextField('Pechos')
    accessory_muscle_use= models.CharField('Tamaño', max_length=100)
    respiratory_rate  = models.CharField('Frecuencia Respiratoria', max_length=1, default='N', choices=RESPIRATORY_RATE_CHOICE)
    tour_freely = models.CharField('Excursion de Bases', max_length=100)
    tour_vertices = models.CharField('Excursion de Vertices', max_length=100)
    jars_vibrations = models.CharField('Vibraciones Vocales', max_length=100)
    sonority = models.CharField('Sonoridad', max_length=100)
    vesicular_murmur = models.CharField('Murmullo Vesicular', max_length=100)
    rales_moist_rales = models.CharField('Rales crepitantes húmedos ', max_length=100)
    roncus = models.CharField('Roncus', max_length=100)
    wheezing = models.CharField('Sibilancias', max_length=100)
    tubal_puff = models.CharField('Soplo Tubario', max_length=100)
    pleural_rub = models.CharField('Frote Pleural', max_length=100)
    comments = models.TextField('Observaciones')



class CardiovascularSystemExam(models.Model):
    patient = models.ForeignKey(User) #fk
    date = models.DateField("Fecha del Examen", auto_now_add=True)

    beats = models.CharField('Latidos', max_length=100)
    shock_tip = models.CharField('Choques de Punta', max_length=100)
    R1 = models.CharField('R1', max_length=100)
    R2 = models.CharField('R2', max_length=100)
    R3 = models.CharField('R3', max_length=100)
    R4 = models.CharField('R4', max_length=100)
    puffs = models.CharField('Murmullo Vesicular', max_length=100)
    clicks= models.CharField('Chasquidos', max_length=100)
    carotid_pulse = models.IntegerField('Pulso Carotídeo')
    humeral_pulse = models.IntegerField('Pulso Humeral ')
    radial_pulse = models.IntegerField('Pulso Radial ')
    femoral_pulse = models.IntegerField('Pulso Femoral ')
    popliteal_pulse = models.IntegerField('Pulso Poplíteo')
    posterior_tibial_pulse = models.IntegerField('Pulso Tibial posterior ')
    pedius_pulse = models.IntegerField('Pulso Pedio')
    comments = models.TextField('Observaciones')



class Relation(models.Model):
    """
        Para Definir las relaciones de Parentesco entre Familiares
    """
    patient = models.ForeignKey(User, related_name="paciente_user")
    kin = models.ForeignKey(User, verbose_name='Pariente', related_name="familiar_user")
    type_relation = models.IntegerField('Tipo Parentesco', default=0, choices=RELATIONS_CHOICES)

    class Meta:
        db_table = "Relations"



class HereditaryDisease(models.Model):
    """
        Enfermedades Hereditarias que padece el paciente
    """
    patient = models.ForeignKey(User)
    type = models.IntegerField('Tipo', default=0, choices=HEREDITARY_DISEASES)
    name = models.CharField('Nombre', max_length=100)

    class Meta:
        db_table = "HereditaryDiseases"


