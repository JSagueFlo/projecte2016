from django.conf.urls import url, include
from django.contrib import admin
import docutils
from main.views import *

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),

    url(r'^$', home),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^signup/$', signup),
    url(r'^codi/$', codi),
    url(r'^change_password/$', change_password),
    url(r'^dashboard/$', dashboard),
    url(r'^dashboard/elimina_centre/([0-9]+)/$', elimina_centre),
    url(r'^dashboard/elimina_user/$', elimina_user),

    url(r'^pagines/(.+)/$', pagines),
    #url('^', include('django.contrib.auth.urls')),
    url(r'^centres/$', centres),
    url(r'^centre/([0-9]+)/$', centre),
    url(r'^centre/([0-9]+)/([0-9]+)/$', boia),
    url(r'^centre/([0-9]+)/([0-9]+)/([0-9]+)/$', boia_any),
    url(r'^centre/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)/$', boia_mes),
    url(r'^centre/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)/$', boia_dia),
]
