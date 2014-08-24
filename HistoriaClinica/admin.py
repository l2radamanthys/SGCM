#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from HistoriaClinica import models


#establesco las tablas que seran modificadas por el admin
admin.site.register(models.Image)
admin.site.register(models.File)
admin.site.register(models.AntecedentesPerinatales)
admin.site.register(models.ToxicHabits)
admin.site.register(models.BasicExam)
admin.site.register(models.HeadExam)
admin.site.register(models.NeckExam)
admin.site.register(models.PFTSExam)
admin.site.register(models.OsteoArticularExam)
admin.site.register(models.RespiratorySystemExam)
admin.site.register(models.CardiovascularSystemExam)
admin.site.register(models.Relation)
admin.site.register(models.HereditaryDisease)
#admin.site.register(models.)
