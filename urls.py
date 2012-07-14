from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from settings import MEDIA_ROOT
import views as base_views
import GestionTurnos.users_views as gt_users_views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SGCM.views.home', name='home'),
    # url(r'^SGCM/', include('SGCM.foo.urls')),

	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, 'show_indexes': True }),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^$', base_views.index),
    (r'^index/$', base_views.index),
    (r'^login/$', base_views.login),
    (r'^logout/$', base_views.logout),

    # Usuarios Registrar
    (r'^usuarios/registrar/$', gt_users_views.register),
    
    

)
