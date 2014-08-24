#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from GestionTurnos import models


#establesco las tablas que seran modificadas por el admin
admin.site.register(models.UserInformation)
admin.site.register(models.MedicalSpecialties)
admin.site.register(models.MedicalSpecialityFor)
admin.site.register(models.BusinessHours)
admin.site.register(models.DayOfAttention)
admin.site.register(models.Turn)
admin.site.register(models.Message)
admin.site.register(models.NonWorkingDay)
admin.site.register(models.MedicalConsultation)
admin.site.register(models.MedicalPrescription)
#admin.site.register(models.)
