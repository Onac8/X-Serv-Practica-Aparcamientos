from django.conf.urls import include, url
from django.contrib import admin
from aparcamientos import views
from myproject import settings
from django.views.static import *

urlpatterns = [
    url(r'^static/(?P<path>.*)$',serve,{'document_root':settings.STATIC_URL}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name="Pagina Principal"),
    url(r'^login', views.loginPS, name="Pagina de entrada a PS"),
    url(r'^logout', views.logoutPS, name="Pagina de desconexion de PS"),

    #url(r'^annotated/(.+)', views.template, name="Pagina del recurso con template"),
    #url(r'^(.+)', views.resource, name="Pagina del recurso"),
]
