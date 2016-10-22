# -*- coding: utf-8 -*-
"""gestion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from sistema.views import buscar
from sistema.views import contactos
from sistema.views import solicitudes
from sistema.views import home
from sistema.views import javascript
from sistema.views import despachar
from sistema.views import llegada
from gestion import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^buscar/$', buscar, name="buscar"),
    url(r'^contactos/$', contactos),    
    url(r'^login/$', views.login_page, name="login"),
    url(r'^$', views.home_page, name="homepage"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^home/$', home, name="home"),
    url(r'^login/solicitud/$', solicitudes, name="solicitudes"),
    url(r'^login/solicitud/(?P<cod_ruta>.*)$', despachar, name="despachar"),
    url(r'^login/llegada/(?P<num_bus>.*)$', llegada, name="llegada"), 
    url(r'^javascript$', javascript, name="javascript"),


]
