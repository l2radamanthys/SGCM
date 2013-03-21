#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Script para inicializar el Sistema
    ----------------------------------

    Ejecutar despues de haver creado las Tablas del Sistema

    Este Script Ejecuta Inserciones Basicas en Las Tablas por lo que
    es recomendable Ejecutarlo solo una ves.. posteriores ejecuciones pueden
    crear conflictos en la Base de Datos
    $ shell -c "include init_app"

"""

from settings import *
from django.conf.urls.defaults import *
from django.contrib.auth.models import User, Group
from GestionTurnos.models import *
import datetime

#nombre de usuario que se le definio al Admin cuando se creo las tablas
admin_username = "admin"

print """
-----------------------------------------------
        SGCM Inicializando datos
-----------------------------------------------

"""

print "Inicializando Datos de Interfaz.......",
patient_group = Group(name="Paciente")
patient_group.save()
print "..",
medic_group = Group(name="Medico")
medic_group.save()
print "..",
admin_group = Group(name="Administrativo")
admin_group.save()
print "OK"

print "Creando los Datos del Admin...............",
adm = User.objects.get(username=admin_username)
adm.first_name = "Admin"
adm.last_name = "Site"
adm.groups.add(admin_group)
adm.save()
adm_data = UserInformation(
    user = adm,
    birth_date = datetime.date.today(),
)
adm_data.save()


print "OK"
print "\n-----------------------------------------------"
