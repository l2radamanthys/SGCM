
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin


from settings import MEDIA_ROOT
import views as base_views
import debug_views
#gestion de turnos
import GestionTurnos.patients_views as gt_patients_views
import GestionTurnos.medics_views as gt_medics_views
import GestionTurnos.messages_views as gt_messages_views
import GestionTurnos.admins_views as gt_admins_views
#historia clinica
import HistoriaClinica.medics_views as hc_medics_views

#django tareas programadas
import django_cron
django_cron.autodiscover()

#habilitar el administrado
admin.autodiscover()

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
    (r'^change-password/$', base_views.change_password),
    (r'^restricted-access/$', base_views.restricted_access),
    (r'^restricted-access/(.+)/$', base_views.restricted_access),
    (r'^nuevo-paciente/$', gt_patients_views.patient_register),
    (r'^activar-usuario/(.+)/(.+)/$', gt_patients_views.patient_activate),
    (r'^activar-usuario/$', gt_patients_views.patient_activate),
    (r'^mis-datos/$', base_views.my_info),
    (r'^cambiar-avatar/$', base_views.change_my_avatar),
    (r'^modificar-datos-personales/$', base_views.change_my_info),

    ## - Gestion de Turnos Views - ##

    ## Admins Viewws
    (r'^admins/registrar/medico/$', gt_admins_views.admin_add_medic),
    (r'^admins/buscar/medico/$', gt_admins_views.admin_search_medic),
    (r'^admins/mostrar/medico/(.+)/$', gt_admins_views.admin_show_medic),
    (r'^admins/agregar/medico/expecialidad/(.+)/$', gt_admins_views.admin_add_medic_expeciality),
    (r'^admins/modificar/medico/(\w+)/$', gt_admins_views.admin_edit_medic),

    (r'^admins/registrar/administrativo/$', gt_admins_views.admin_add_admin),
    (r'^admins/buscar/administrativo/$', gt_admins_views.admin_search_admin),
    (r'^admins/mostrar/administrativo/(.+)/$', gt_admins_views.admin_show_admin),
    (r'^admins/modificar/administrativo/(.+)/$', gt_admins_views.admin_edit_admin),

    (r'^admins/buscar/paciente/$', gt_admins_views.admin_search_patient),
    (r'^admins/mostrar/paciente/(.+)/$', gt_admins_views.admin_show_patient),
    (r'^admins/modificar/paciente/(.+)/$', gt_admins_views.admin_edit_patient),
    (r'^admins/modificar/user-password/(.+)/$', gt_admins_views.admin_change_patient_password),
    (r'^admins/modificar/medic-password/(.+)/$', gt_admins_views.admin_change_medic_password),
    (r'^admins/modificar/admin-password/(.+)/$', gt_admins_views.admin_change_admin_password),

    #asignar turno
    (r'^admins/selecionar-medico/turno-paciente/(.+)/$', gt_admins_views.admin_patient_turn_set_medic),
    (r'^admins/selecionar-dia/turno/(\w+)/(\w+)/$', gt_admins_views.admin_select_date_medic_turn),
    (r'^admins/selecionar-dia/turno/(\w+)/(\w+)/(\d{1,2})/(\d{4})/$', gt_admins_views.admin_select_date_medic_turn),
    (r'^admins/agregar/turno/(\w+)/(\w+)/(\d{1,2})/(\d{1,2})/(\d{4})/$', gt_admins_views.admin_new_turn),
    (r'^admins/actualizar/turno-paciente/(\d+)/$', gt_admins_views.admin_update_patient_turn),
    (r'^admins/actualizar/turno-medico/(\d+)/$', gt_admins_views.admin_update_medic_turn),
    (r'^admins/mostrar/turno-paciente/(\d+)/$', gt_admins_views.admin_show_patient_turn),
    (r'^admins/mostrar/turno-medico/(\d+)/$', gt_admins_views.admin_show_medic_turn),
    (r'^admins/listado/turno-medico/(\w+)/$', gt_admins_views.admin_show_medic_turn_list),
    (r'^admins/turnos/imprimir/(\d{1,2})/$',  gt_admins_views.turn_pdf), #imprimir comprobante turno

    #expecialidades
    (r'^admins/listado/expecialidad-medica/$', gt_admins_views.admin_list_expecialities),
    (r'^admins/mostrar/expecialidad-medica/(\d{1,2})/$', gt_admins_views.admin_show_expeciality),
    (r'^admins/registrar/expecialidad-medica/$', gt_admins_views.admin_add_expeciality),
    #quita una expecialidad asignada a un medico
    (r'^admins/borrar/expecialidad-del-medico/(\w+)/(\d+)/$', gt_admins_views.admin_delete_medic_expeciality),
    #####

    (r'^pacientes/buscar/$', gt_medics_views.patients_search),
    (r'^pacientes/registrar/$', gt_medics_views.patient_register),
    (r'^pacientes/show-info/(.+)/$', gt_medics_views.patient_show_info),
    (r'^pacientes/modificar-datos-basicos/(.+)/$', gt_medics_views.patient_edit_basic_info),

    ## consultas medicas
    (r'^pacientes/mostrar/consultas-medicas/(.+)/$', gt_medics_views.patient_show_medical_consultation),
    (r'^medicos/agregar/consulta-medica/(.+)/$', gt_medics_views.my_add_medical_consultation),
    (r'^medicos/mostrar/consulta-medica/(\d{1,2})/$', gt_medics_views.my_show_medical_consultation),
    (r'^medicos/modificar/consulta-medica/(\d{1,2})/$', gt_medics_views.my_edit_medical_consultation),
    (r'^medicos/borrar/consulta-medica/(\d{1,2})/$', gt_medics_views.my_delete_medical_consultation),

    ## recetas
     (r'^medicos/listado/prescripcion-medica/(.+)/$', gt_medics_views.medic_list_patient_prescriptions),
     (r'^medicos/agregar/prescripcion-medica/(\d{1,2})/$', gt_medics_views.medic_add_patient_prescription),
     (r'^medicos/mostrar/prescripcion-medica/(\d{1,2})/$', gt_medics_views.medic_show_patient_prescription),
     (r'^medicos/imprimir/prescripcion-medica/(\d{1,2})/$', gt_medics_views.medical_prescription_pdf),

    # Horario de Atencion
    (r'^medicos/mostrar/mis-horarios-atencion/$', gt_medics_views.my_medic_show_business_hours),
    (r'^medicos/agregar/mi-horario-atencion/$', gt_medics_views.my_medic_add_business_hours),
    (r'^medicos/borrar/mi-horarios-atencion/(\d{1,2})/$', gt_medics_views.my_medic_del_business_hours),
    (r'^medicos/mostrar/dias-no-laborales/$', gt_medics_views.my_medic_show_nonworking_days),
    (r'^medicos/mostrar/dias-no-laborales/(\d{1,2})/(\d{4})/$', gt_medics_views.my_medic_show_nonworking_days),
    (r'^medicos/agregar/dia-no-laboral/(\d{1,2})/(\d{1,2})/(\d{4})/$', gt_medics_views.my_medic_add_nonworking_day),
    (r'^medicos/borrar/dia-no-laboral/(\d{1,2})/(\d{1,2})/(\d{4})/$', gt_medics_views.my_medic_del_nonworking_day),
    (r'^medicos/selecionar/turnos-asignados/$', gt_medics_views.select_date_to_show_turns),
    (r'^medicos/selecionar/turnos-asignados/(\d{1,2})/(\d{4})/$', gt_medics_views.select_date_to_show_turns),
    (r'^medicos/mostrar/turnos-asignados/$', gt_medics_views.show_turns),
    (r'^medicos/mostrar/turnos-asignados/(\d{1,2})/(\d{1,2})/(\d{4})/$', gt_medics_views.show_turns),
    (r'^medicos/cronograma/$', gt_medics_views.show_cronogram),
    (r'^medicos/listado/$', gt_patients_views.patient_show_medics_list),
    (r'^medicos/mostrar/(\d{1,2})/$', gt_patients_views.patient_show_medic_info),

    # gestion turnos
    (r'^pacientes/turnos/selecionar-dia/(\d{1,2})/$', gt_patients_views.patient_new_turn_day_select), #selecion fecha para solicitar turno
    (r'^pacientes/turnos/selecionar-dia/(\d{1,2})/(\d{1,2})/(\d{4})/$', gt_patients_views.patient_new_turn_day_select), #selecion fecha para solicitar turno
    (r'^pacientes/turnos/agregar/(\d{1,2})/(\d{1,2})/(\d{1,2})/(\d{4})/$', gt_patients_views.patient_new_turn),
    (r'^pacientes/turnos/listado/$',  gt_patients_views.patient_show_turn_request), #mostrar estado turnos solicitados
    (r'^pacientes/turnos/mostrar/(\d{1,2})/$',  gt_patients_views.patient_show_turn_detail ), #detalle turno especifico
    (r'^pacientes/turnos/cancelar/(\d{1,2})/$',  gt_patients_views.patient_turn_cancel), #cancelar turno
    (r'^pacientes/turnos/imprimir/(\d{1,2})/$',  gt_patients_views.patient_turn_pdf), #imprimir comprobante turno

    #turnos asignados medico
    (r'^medicos/turnos/seleccionar-dia/(.+)/$', gt_medics_views.medic_new_turn_day_select), #selecion fecha para solicitar turno
    (r'^medicos/turnos/seleccionar-dia/(.+)/(\d{1,2})/(\d{4})/$', gt_medics_views.medic_new_turn_day_select), #selecion fecha para solicitar turno
    (r'^medicos/turnos/agregar/(\d{1,2})/(\d{1,2})/(\d{1,2})/(\d{4})/$', gt_medics_views.medic_new_turn),
    (r'^medicos/turnos/listado/(.+)/$',  gt_medics_views.medic_show_patient_turn_request), #mostrar estado turnos solicitados
    (r'^medicos/turnos/mostrar/(\d{1,2})/$',  gt_medics_views.medic_show_patient_turn_detail), #detalle turno especifico
    (r'^medicos/turnos/cancelar/(\d{1,2})/$',  gt_medics_views.medic_turn_cancel), #cancelar turno
    (r'^medicos/turnos/reactivar/(\d{1,2})/$', gt_medics_views.medic_turn_reset),

    #mensajes internos
    (r'^mensajes/redactar/$', gt_messages_views.send_message),
    (r'^mensajes/responder/(\d{1,5})/$', gt_messages_views.re_send_message), #responder
    (r'^mensajes/recibidos/$', gt_messages_views.received),
    (r'^mensajes/mostrar/(\d{1,2})/$', gt_messages_views.read),
    (r'^mensajes/borrar/(\d{1,2})/$', gt_messages_views.delete),
    (r'^medicos/nueva/consulta-online/(\d{1,2})/$', gt_patients_views.patient_set_medic_consulation), #paciente realizar consulta al medico

    (r'^mensajes/enviados/$', gt_messages_views.sent),

    ## - Historia Clinica Views - ##

    #imagenes
    (r'^pacientes/mostrar/imagenes/(.+)/$', hc_medics_views.medic_list_patients_images),
    (r'^pacientes/agregar/imagen/(.+)/$', hc_medics_views.medic_add_patients_images),
    (r'^pacientes/borrar/imagen/(\d{1,2})/$', hc_medics_views.medic_del_patient_image),
    (r'^pacientes/modificar/imagen/(\d{1,2})/$', hc_medics_views.medic_edit_patient_image),

    #archivos
    #borrado no se incluira
    #(r'^pacientes/listado/archivos/(.+)/$', hc_medics_views.medic_list_patient_files),

    #antecedentes perinatales (hecho)
    (r'^pacientes/mostrar/antecedentes-perinatales/(.+)/$', hc_medics_views.medic_view_patient_perinatal_antecedents),
    (r'^pacientes/modificar/antecedentes-perinatales/(.+)/$',hc_medics_views.medic_edit_patient_perinatal_antecedents),

    #habitos toxicos (hecho)
    (r'^pacientes/mostrar/habitos-toxicos/(.+)/$', hc_medics_views.medic_view_patient_toxic_habits),
    (r'^pacientes/modificar/habitos-toxicos/(.+)/$', hc_medics_views.medic_edit_patient_toxic_habits),

    #examenes fisicos
    (r'^pacientes/listado/examen-fisico/(.+)/$', hc_medics_views.medic_list_patient_phisic_exam),
    (r'^pacientes/agregar/examen-fisico/(.+)/$', hc_medics_views.medic_add_patient_phisic_exam),
    (r'^pacientes/mostrar/examen-fisico/(\d{1,2})/$', hc_medics_views.medic_show_patient_phisic_exam),
    (r'^pacientes/borrar/examen-fisico/(\d{1,2})/$', hc_medics_views.medic_del_patient_phisic_exam),

    #examen cabeza
    (r'^pacientes/listado/examen-cabeza/(.+)/$', hc_medics_views.medic_list_patient_head_exam),
    (r'^pacientes/agregar/examen-cabeza/(.+)/$', hc_medics_views.medic_add_patient_head_exam),
    (r'^pacientes/mostrar/examen-cabeza/(\d{1,2})/$', hc_medics_views.medic_show_patient_head_exam),
    (r'^pacientes/borrar/examen-cabeza/(\d{1,2})/$', hc_medics_views.medic_del_patient_head_exam),

     #Examenes de Cuello
     (r'^pacientes/listado/examen-cuello/(.+)/$', hc_medics_views.medic_list_patient_neck_exam),
     (r'^pacientes/agregar/examen-cuello/(.+)/$', hc_medics_views.medic_add_patient_neck_exam),
     (r'^pacientes/mostrar/examen-cuello/(\d{1,2})/$', hc_medics_views.medic_show_patient_neck_exam),
     (r'^pacientes/borrar/examen-cuello/(\d{1,2})/$', hc_medics_views.medic_del_patient_neck_exam),

    #EXAMEn piel faneras y tejido subcutaneo
    (r'^pacientes/listado/examen-piel-faneras/(.+)/$', hc_medics_views.medic_list_patient_pfts_exam),
    (r'^pacientes/agregar/examen-piel-faneras/(.+)/$', hc_medics_views.medic_add_patient_pfts_exam),
    (r'^pacientes/mostrar/examen-piel-faneras/(\d{1,2})/$', hc_medics_views.medic_show_patient_pfts_exam),
    (r'^pacientes/borrar/examen-piel-faneras/(\d{1,2})/$', hc_medics_views.medic_del_patient_pfts_exam),

    #Examen Sistema Osteo Articular
    (r'^pacientes/listado/examen-osteo-articular/(.+)/$', hc_medics_views.medic_list_patient_osteo_art_exam),
    (r'^pacientes/agregar/examen-osteo-articular/(.+)/$', hc_medics_views.medic_add_patient_osteo_art_exam),
    (r'^pacientes/mostrar/examen-osteo-articular/(\d{1,2})/$', hc_medics_views.medic_show_patient_osteo_art_exam),
    (r'^pacientes/borrar/examen-osteo-articular/(\d{1,2})/$', hc_medics_views.medic_del_patient_osteo_art_exam),

    #Examen Aparato Respiratorio
    (r'^pacientes/listado/examen-aparato-respiratorio/(.+)/$', hc_medics_views.medic_list_patient_resp_system_exam),
    (r'^pacientes/agregar/examen-aparato-respiratorio/(.+)/$', hc_medics_views.medic_add_patient_resp_system_exam),
    (r'^pacientes/mostrar/examen-aparato-respiratorio/(\d{1,2})/$', hc_medics_views.medic_show_patient_resp_system_exam),
    (r'^pacientes/borrar/examen-aparato-respiratorio/(\d{1,2})/$', hc_medics_views.medic_del_patient_resp_system_exam),

    (r'^pacientes/listado/examen-aparato-cardiovascular/(.+)/$', hc_medics_views.medic_list_patient_cardio_exam),
    (r'^pacientes/agregar/examen-aparato-cardiovascular/(.+)/$', hc_medics_views.medic_add_patient_cardio_exam),
    (r'^pacientes/mostrar/examen-aparato-cardiovascular/(\d{1,2})/$', hc_medics_views.medic_show_patient_cardio_exam),
    (r'^pacientes/borrar/examen-aparato-cardiovascular/(\d{1,2})/$', hc_medics_views.medic_del_patient_cardio_exam),

    #Grupo Familiar
    (r'^pacientes/mostrar/grupo-familiar/(\w+)/$', hc_medics_views.medic_show_patient_family_menbers),
    (r'^pacientes/agregar/grupo-familiar/(\w+)/$', hc_medics_views.medic_add_patient_family_member),

    ######################################################################################
    #debug views, this views only desing for testing
    (r'^perms/$', debug_views.perms_list),
    (r'^apps/$', debug_views.apps_list),
    (r'^usuarios/calendar/$', debug_views.calendar),
    #(r'^usuarios/calendar/(\d{1,2})/(\d{4})/$', debug_views.calendar),



)
