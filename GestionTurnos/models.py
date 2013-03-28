#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

#replaced by easy_thumbs, django-thumbs only found in Dj 1.1 o low
#from libs.thumbs import ImageWithThumbsField as ImgThumbsField

import datetime

from globals import *



class UserInformation(models.Model):
    """
        Informacion adicional de usuario
    """
    user = models.ForeignKey(User, unique=True) #Fk

    type_doc = models.CharField(max_length=6, default='---', choices=TYPE_DOC_CHOICE)
    nro_doc = models.CharField(max_length=12, default='')
    gender = models.CharField(max_length=1, default='-', choices=SEXO_CHOICE)
    phone = models.CharField(max_length=20, default='No Definido')
    address = models.CharField(max_length=120, default='No Definido')
    city = models.CharField(max_length=120, default='No Definido')
    state = models.CharField(max_length=120, default='No Definido')
    birth_date = models.DateField()
    photo = models.ImageField(upload_to='upload/images', default='upload/images/no-avatar.png')

    #solo para los medicos
    matricula = models.CharField(max_length=30, default='No Medic')


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
    """
        Especialidades Medicas
    """
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
    #tiene que hacer referencia a un medico
    user = models.ForeignKey(User)
    #tiene q referenciar una especialidad
    speciality = models.ForeignKey(MedicalSpecialties)


    class Meta:
        db_table = "MedicalSpecialtiesFor"
        verbose_name = "Medical Specialty For"
        verbose_name_plural = "Medical Specialties For"
        permissions = (
            #identificador      #descripcion
            ("show_medical_speciality_for",  "Mostrar Mi Informacion"),
        )


    def speciality_name(self):
        return '%s' %(self.speciality.name)


    def medic_name(self):
        return '%s' %(self.user.username)


    def __unicode__(self):
        return '%s - %s' %(self.user.username, self.speciality.name)



class BusinessHours(models.Model):
    """
        Horarios de Atencion
    """
    user = models.ForeignKey(User) #tiene que hacer referencia a un medico
    date = models.IntegerField('Dia', default=1, choices=DATE_CHOICE)
    start_time = models.TimeField('Hora de Inicio Turno')
    end_time = models.TimeField('Hora de Fin Turno')
    turn_duration = models.IntegerField('Duracion Turno en Minutos', default=20)


    class Meta:
        db_table = "BusinessHours"
        permissions = (
            #identificador      #descripcion
            ("show_Business_Hours",  "Mostrar Horario Atencion"),
        )


    def calculate_interval_minutes(self):
        """
            Calcula la cantidad de minutos entre los 2 intervalos
        """
        #implementado directamente abajo :S
        pass


    def str_day(self):
        return DATE_CHOICE[self.date-1][1]


    def number_of_turns(self):
        """
            Retorna el numero de turnos que se pueden asignar en dicho horario
            de atencion
        """
        start = datetime.timedelta(hours=start_time.hour, minutes=self.start_time.minute)
        end = datetime.datetime(hours=self.end_time.hours, minutes=self.end_time.minute)
        dif = end - start
        min = dif.seconds / 60  #calcula el numero de minutos
        n_turns = min / self.turn_duration #calcula el numero de turnos por rendondeo
        return n_turns



class Message(models.Model):
    """
        Clase Para Manejar mensajes entre usuarios
    """
    from_user = models.ForeignKey(User, related_name='from_user')
    to_user = models.ForeignKey(User, related_name='to_user')
    date = models.DateTimeField(auto_now_add=True)
    issue = models.CharField(max_length=125, default='')
    content = models.TextField()
    read = models.BooleanField(default=False)


    class Meta:
        db_table = "Messages"
        verbose_name = "InboxMessage"
        verbose_name_plural = "InboxMessages"



class NonWorkingDay(models.Model):
    """
	Dia no laborales
    """
    date = models.DateField()  #fecha
    issue = models.TextField() #asunto
    user = models.ForeignKey(User, related_name='from')

    class Meta:
        db_table = "NonWorkingDays"



class MedicalConsultation(models.Model):
    """
	Consulta Medica
    """
    medic = models.ForeignKey(User, related_name='medic_user')
    patient = models.ForeignKey(User, related_name='patient_user')
    date = models.DateTimeField(auto_now_add=True)
    issue = models.TextField(default='') #motivo
    diagnostic = models.TextField(default='') #diagnostico
    physical_exam = models.TextField(default='') #examen fisico
    observations = models.TextField(default='') #observaciones

    class Meta:
        db_table = "MedicalConsultation"
