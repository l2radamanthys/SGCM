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
    matricula = models.CharField(max_length=30) #solo para los medicos

    user = models.ForeignKey(User, unique=True)


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


    def __unicode__(self):
        return "%s - User Information" %self.user.username


    def doc(self):
        return "%s - %s" %(self.nro_doc, self.type_doc)



class MedicalSpecialties(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()


    class Meta:
        db_table = "MedicalSpecialties"
        verbose_name = "Medical Specialty"
        verbose_name_plural = "Medical Specialties"
        permissions = (
            #identificador      #descripcion
            ("show_medical_speciality",  "Mostrar Mi Informacion"),
        )


    def __unicode__(self):
        return self.name



class MedicalSpecialityFor(models.Model):
    """
        Tendria que haber sido un many to many en UserInfo pero no queria sobrecargarlo
        ya que solo se usa en los medicos por lo que lo defini directamente.
    """
    user = models.ForeignKey(User) #tiene que hacer referencia a un medico
    speciality = models.ForeignKey(MedicalSpecialties) #tiene


    class Meta:
        db_table = "MedicalSpecialtiesFor"
        verbose_name = "Medical Specialty For"
        verbose_name_plural = "Medical Specialties For"
        permissions = (
            #identificador      #descripcion
            ("show_medical_speciality_for",  "Mostrar Mi Informacion"),
        )