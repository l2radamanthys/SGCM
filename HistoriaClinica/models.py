#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User

from libs.thumbs import ImageWithThumbsField as ImgThumbsField

import datetime
from globals import *



class Image(model.Model):
    """
	Imagenes Subidas
    """
    date = models.DateField(auto_now_add=True)
    medic = models.ForeignKey(User, related_name='medic_user')
    patient = models.ForeignKey(User, related_name='patient_user')
    title = model.CharField(max_length=125, default='')
    content = model.TextField(default='')
    image = ImgThumbsField(upload_to='upload/images')



class File(model.Model):
    """
	Archivos Subidos
    """
    date = models.DateField(auto_now_add=True)
    medic = models.ForeignKey(User, related_name='medic_user')
    patient = models.ForeignKey(User, related_name='patient_user')
    title = model.CharField(max_length=125, default='')
    content = model.TextField(default='')
    image = FileField(upload_to='upload/files')