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
    medic = models.ForeignKey(User, related_name='medic_user')
    patient = models.ForeignKey(User, related_name='patient_user')
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
    medic = models.ForeignKey(User, related_name='medic_user')
    patient = models.ForeignKey(User, related_name='patient_user')
    title = models.CharField(max_length=125, default='')
    content = models.TextField(default='')
    archive = models.FileField(upload_to='upload/files')


    class Meta:
        db_table = "Files"