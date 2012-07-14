#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from GestionTurnos import models


#establesco las tablas que seran modificadas por el admin
admin.site.register(models.UserInformation)


