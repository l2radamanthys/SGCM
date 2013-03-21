
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

from settings import MEDIA_ROOT
import views as base_views
import debug_views
#gestion de turnos
import GestionTurnos.users_views as gt_users_views
import GestionTurnos.medics_views as gt_medics_views
import GestionTurnos.messages_views as gt_messages_views
import GestionTurnos.patients_views as gt_patients_views
#historia clinica
import HistoriaClinica.medics_views as hc_medics_views


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
    (r'^restricted-access/$', base_views.restricted_access),
    (r'^restricted-access/(.+)/$', base_views.restricted_access),
    (r'^nuevo-paciente/$', gt_patients_views.patient_register),
    (r'^mis-datos/$', base_views.my_info),

    ## - Gestion de Turnos Views - ##

    (r'^pacientes/buscar/$', gt_medics_views.patients_search),
    (r'^pacientes/registrar/$', gt_medics_views.patient_register),
    (r'^pacientes/show-info/(.+)/$', gt_medics_views.patient_show_info),
    (r'^pacientes/modificar-datos-basicos/(.+)/$', gt_medics_views.patient_edit_basic_info),
    (r'^pacientes/mostrar/consultas-medicas/(.+)/$', gt_medics_views.patient_show_medical_consultation),
    (r'^medicos/agregar/consulta-medica/(.+)/$', gt_medics_views.my_add_medical_consultation),
    #(r'^medicos/mostrar/consulta-medica/(\d{1,2})/$', gt_medics_views.my_show_medical_consultation),
    (r'^medicos/modificar/consulta-medica/(\d{1,2})/$', gt_medics_views.my_edit_medical_consultation),
    (r'^medicos/borrar/consulta-medica/(\d{1,2})/$', gt_medics_views.my_delete_medical_consultation),


    (r'^medicos/mostrar/mis-horarios-atencion/$', gt_medics_views.my_medic_show_business_hours),
    (r'^medicos/agregar/mi-horario-atencion/$', gt_medics_views.my_medic_add_business_hours),
    (r'^medicos/borrar/mi-horarios-atencion/(\d{1,2})/$', gt_medics_views.my_medic_del_business_hours),
    (r'^medicos/mostrar/dias-no-laborales/$', gt_medics_views.my_medic_show_nonworking_days),
    (r'^medicos/mostrar/dias-no-laborales/(\d{1,2})/(\d{4})/$', gt_medics_views.my_medic_show_nonworking_days),
    (r'^medicos/agregar/dia-no-laboral/(\d{1,2})/(\d{1,2})/(\d{4})/$', gt_medics_views.my_medic_add_nonworking_day),
    (r'^medicos/borrar/dia-no-laboral/(\d{1,2})/(\d{1,2})/(\d{4})/$', gt_medics_views.my_medic_del_nonworking_day),

    ## - Historia Clinica Views - ##
    (r'^pacientes/mostrar/imagenes/(.+)/$', hc_medics_views.medic_show_patients_images), #muestra el listado de imagenes


    #debug views, this views only desing for testing
    (r'^perms/$', debug_views.perms_list),
    (r'^apps/$', debug_views.apps_list),
    (r'^usuarios/calendar/$', debug_views.calendar),
    (r'^usuarios/calendar/(\d{1,2})/(\d{4})/$', debug_views.calendar),


)
