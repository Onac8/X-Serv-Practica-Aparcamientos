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
    url(r'^aparcamientos$', views.aparcamientosPS, name="Pagina con todos los aparcamientos"),
    url(r'^aparcamientos/(\w+)', views.infoAparcamiento, name="Muestra todos los datos de un Parking"),
    url(r'^about$', views.aboutPS, name="Pagina de ayuda"),
    url(r'^(.+)', views.gestionUsuario, name="Pagina personal de login users"),
]
