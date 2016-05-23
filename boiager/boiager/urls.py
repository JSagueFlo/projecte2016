from django.conf.urls import url, include
from django.contrib import admin
from main.views import *

urlpatterns = [
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
    url(r'^centres/$', centres),
    url(r'^centre/([0-9]+)/$', centre),
    url(r'^centre/([0-9]+)/([0-9]+)/$', boia),
    url(r'^centre/([0-9]+)/([0-9]+)/([0-9]+)/$', boia_any),
    url(r'^centre/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)/$', boia_mes),
    url(r'^centre/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)/$', boia_dia),
]
