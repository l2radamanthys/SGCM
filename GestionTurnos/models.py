#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from globals import *


class UserInformation(models.Model):
    type_doc = models.CharField(max_length=6, default='---', choices=TYPE_DOC_CHOICE)
    nro_doc = models.CharField(max_length=12, default='')
    gender = models.CharField(max_length=1, default='-', choices=SEXO_CHOICE)
    phone = models.CharField(max_length=20, default='No Definido')
    address = models.CharField(max_length=120, default='No Definido')

    #solo para los medicos
    matricula = models.CharField(max_length=30)

    user = models.ForeignKey(User, unique=True)


    def __unicode__(self):
        return "%s - User Information" %self.user.username

    def doc(self):
        return "%s - %s" %(self.nro_doc, self.type_doc)


    class Meta:
        db_table = "UsersInformation"
        verbose_name = "User Information"
        verbose_name_plural = "User's Information"
        permissions = (
            #identificador      #descripcion
            ("user_show",  "Mostrar Mi Informacion"),
            ("all_med_show",  "Ver Informacion de Medico"),
            ("med_pac_show",  "Medico Ver Informacion Paciente"),
        )
