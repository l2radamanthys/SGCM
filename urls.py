
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

from settings import MEDIA_ROOT
import views as base_views
import debug_views
import GestionTurnos.users_views as gt_users_views
import GestionTurnos.medics_views as gt_medics_views
import GestionTurnos.inbox_views as gt_inbox_views

import GestionTurnos.patients_views as gt_patients_views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SGCM.views.home', name='home'),
    # url(r'^SGCM/', include('SGCM.foo.urls')),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, 'show_indexes': True }),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


    ## - Basic Views - ##

    (r'^$', base_views.index),
    (r'^index/$', base_views.index),
    (r'^login/$', base_views.login),
    (r'^logout/$', base_views.logout),
    #(r'^change-password/$', base_views.change_password), #por algun motivo no me esta cambiando las contrasenia revisar
    #(r'^restricted-access/$', base_views.restricted_access),
    #(r'^restricted-access/(.+)/$', base_views.restricted_access),

    ## - Gestion de Turnos Views - ##


    (r'^pacientes/buscar/$', gt_patients_views.search), 
    (r'^pacientes/show-info/(.+)/$', gt_patients_views.show_info),
    (r'^pacientes/registrar/$', gt_users_views.register),
    (r'^pacientes/modificar-datos-basicos/(.+)/$', gt_patients_views.edit_basic_info),


    #(r'^usuarios/mis-datos/$', gt_users_views.show_my_info),

    #inbox
    #(r'^usuarios/inbox/$', gt_inbox_views.received),
    #(r'^usuarios/inbox/(\d{1,2})/$', gt_inbox_views.read),


    #(r'^medicos/registrar/$', gt_medics_views.register),
    #(r'^medicos/buscar/$', gt_medics_views.search),
    #(r'^medicos/listado/$', gt_medics_views.list),
    #(r'^medicos/mostrar/datos/(\d{1,2})/$', gt_medics_views.show_my_info),
    #(r'^medicos/mostrar/especilidades/(\d{1,2})/$', gt_medics_views.show_medic_specialities),
    #(r'^medicos/agregar/especilidades/(\d{1,2})/$', gt_medics_views.add_medic_speciality),
    #(r'^medicos/quitar/especilidades/(\d{1,2})/$', gt_medics_views.del_medic_speciality),
    #(r'^medicos/mostrar/horarios-atencion/(\d{1,2})/$', gt_medics_views.show_medic_business_hours),
    #(r'^medicos/agregar/horario-atencion/(\d{1,2})/$', gt_medics_views.add_medic_business_hours),
    ## - Historia Clinica Views - ##

    #debug views
    (r'^perms/$', debug_views.perms_list),
    (r'^apps/$', debug_views.apps_list),
    (r'^usuarios/calendar/$', debug_views.calendar),
    (r'^usuarios/calendar/(\d{1,2})/(\d{4})/$', debug_views.calendar),


)
