#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

#replaced by easy_thumbs, django-thumbs only found in Dj 1.1 o low
#from libs.thumbs import ImageWithThumbsField as ImgThumbsField

import datetime

from utils import *
from globals import *




class UserInformation(models.Model):
    """
        Informacion adicional de usuario
    """
    user = models.ForeignKey(User, unique=True) #Fk

    type_doc = models.CharField("Tipo Documente", max_length=6, default='---', choices=TYPE_DOC_CHOICE)
    nro_doc = models.CharField("Nro Documento", max_length=12, default='')
    gender = models.CharField("Sexo", max_length=1, default='-', choices=SEXO_CHOICE)
    phone = models.CharField("Telefono", max_length=20, default='No Definido')
    address = models.CharField("Direccion", max_length=120, default='No Definido')
    city = models.CharField("Ciudad", max_length=120, default='No Definido')
    state = models.CharField("Provincia", max_length=120, default='No Definido')
    birth_date = models.DateField("Fecha de Nacimiento")
    photo = models.ImageField("Avatar", upload_to='upload/images', default='upload/images/no-avatar.png')

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


    #def calculate_interval_minutes(self):
        #"""
            #Calcula la cantidad de minutos entre los 2 intervalos
            #*deprecated
        #"""
        ##implementado directamente abajo :S
        #pass


    def str_day(self):
        return DATE_CHOICE[self.date-1][1]


    def number_of_turns(self):
        #"""
            #Retorna el numero de turnos que se pueden asignar en dicho horario
            #de atencion
        #"""
        end_time = time_to_datetime(self.end_time)
        td = time_to_timedelta(self.start_time)
        interval = end_time - td
        minutes = interval.hour * 60 + interval.minute
        n_turns = minutes / self.turn_duration
        return n_turns


    def number_of_turns_bh(self, bh):
        """
            retorna el numero de turnos correspondiente
        """
        end_time = time_to_datetime(bh.end_time)
        td = time_to_timedelta(bh.start_time)
        interval = end_time - td
        minutes = interval.hour * 60 + interval.minute
        n_turns = minutes / bh.turn_duration
        return n_turns


class DayOfAttention(models.Model):
    """
        Dias de Atencion
    """
    business_hour = models.ForeignKey(BusinessHours)
    date = models.DateField('Fecha')
    status = models.IntegerField('Estado', default=0, choices=DAY_OF_ATTENTION_STATUS_CHOICE)
    number_of_turns =  models.IntegerField('Numero de Turnos Asignados', default=0)
    current_end_time = models.TimeField('Horario del Ultimo turno') #hora del ultimo turno


    def get_next_current_end_time(self):
        """
        calcula la hora de fin del proximo nuevo turno

        return:
            next_end_time, overload_turm
        """
        #duracion del turno definido
        t_inc = datetime.timedelta(minutes = self.business_hour.turn_duration)
        current_end_time = time_to_datetime(self.current_end_time)

        _end_time = current_end_time + t_inc
        end_time = datetime_to_time(_end_time)
        #if end_time >= self.business_hour.end_time:
            #return end_time, True
        #else:
            #return end_time, False
        return end_time



    class Meta:
        db_table = "DaysOfAttention"



class Turn(models.Model):
    """
        Turno Asignado
    """
    day = models.ForeignKey(DayOfAttention)
    #aunque hay referencia al medico en day.business_hour.user se implementa medico para acelerar consulta
    medic = models.ForeignKey(User, related_name='medic_user2')
    patient = models.ForeignKey(User, related_name='patient_user2')
    start = models.TimeField('Hora de Inicio Turno') #hora de inicio
    end = models.TimeField('Hora de Fin Turno') #hora prevista de finalizacion
    status = models.IntegerField('Estado', default=0, choices=TURN_STATUS_CHOICE)
    observation = models.TextField('Observaciones')
    number = models.IntegerField('Numero de Turno', default=1)

    class Meta:
        db_table = "Turns"


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



class MedicalPrescription(models.Model):
    """
        Receta Medica

        #Nota: A la hora de mostrar la receta medica debe incluir los datos del
        #medico y del paciente.
    """
    med_consulation = models.ForeignKey(MedicalConsultation)

    prescription_date = models.DateField('Fecha Prescripcion', auto_now_add=True)
    expiration_date = models.DateField('Fecha Vencimiento')
    active_principle = models.CharField('Denominacion Principio Activo',  max_length=30)
    dosage = models.TextField('Dosificacion')
    administration_route = models.CharField('Administrar por via', max_length=1, default='O', choices=VIA_ADMINISTRACION_CHOICE)
    container_format = models.CharField('Formato de Envase',  max_length=45)
    posology = models.IntegerField('Dosificacion en mg')