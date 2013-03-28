#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User

import datetime
from globals import *



class Image(models.Model):
    """
	Imagenes Subidas
    """
    date = models.DateField(auto_now_add=True)
    medic = models.ForeignKey(User, related_name='medic_user0')
    patient = models.ForeignKey(User, related_name='patient_user0')
    title = models.CharField(max_length=125, default='')
    content = models.TextField(default='')
    image = models.ImageField(upload_to='upload/images')


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
