"""boiager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from main.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', home),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^signup/$', signup),
    #url('^', include('django.contrib.auth.urls')),
    url(r'^centres/$', centres),
    url(r'^centre/([0-9]+)/$', centre),
    url(r'^centre/([0-9]+)/([0-9]+)/$', boia),
    #url(r'^centre/<idcentre>/boia/<idboia>/<any>/$', home),
    #url(r'^centre/<idcentre>/boia/<idboia>/<any>/<mes>$', home),
    #url(r'^centre/<idcentre>/boia/<idboia>/<any>/<mes>/<dia>/$', home),
]
