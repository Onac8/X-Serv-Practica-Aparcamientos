from django.conf.urls import include, url
from django.contrib import admin
from aparcamientos import views
from myproject import settings
from django.views.static import *

urlpatterns = [
    url(r'^static/(?P<path>.*)$',serve,{'document_root':settings.STATIC_URL}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name="Pagina principal de PS"),
    url(r'^css/dynamic.css', views.userCss,name='CSS dinamico'),
    url(r'^login', views.loginPS, name="Autentificacion en Parking Simulator"),
    url(r'^logout', views.logoutPS, name="Salida de PS"),
    url(r'^aparcamientos$', views.aparcamientosPS, name="Muestra todos los aparcamientos"),
    url(r'^aparcamientos/(\w+)', views.infoAparcamiento, name="Muestra todos los datos de un Parking"),
    url(r'^about$', views.aboutPS, name="Pagina de ayuda"),
    url(r'^multimedia$', views.multimediaPS, name="Un poco de html5!"),
    url(r'^(.+)/xml$', views.userXml, name='Canal XML de usuario logueado'),
    url(r'^(.+)', views.gestionUsuario, name="Pagina personal de usuarios logueados"),
]
