from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Aparcamientos (models.Model):
    nombre = models.CharField(max_length=70)
    descripcion = models.TextField()
    url = models.URLField(max_length=200)
    accesibilidad = models.IntegerField()
    direccion = models.CharField(max_length=60)
    barrio = models.CharField(max_length=20)
    distrito = models.CharField(max_length=20, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    numComentarios = models.IntegerField(blank=True, default=0)
    email = models.CharField(max_length=50, default="No E-Mail")
    telefono = models.CharField(max_length=40, default="No Tlf")


class Comentario(models.Model):
    #creador = models.ForeignKey(User) --> para futuro voto
    aparcamiento = models.ForeignKey(Aparcamientos)
    texto = models.TextField()

class Personal(models.Model):
    creador = models.OneToOneField(User)
    titulo = models.CharField(max_length=60)
    letra = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)

class Seleccionar (models.Model):
    aparcamiento = models.ForeignKey(Aparcamientos)
    usuario = models.ForeignKey(User)
    fichaPersonal = models.ForeignKey(Personal)
    fecha = models.DateField(auto_now=True)


# class Voto(models.Model):
#     creador = models.ForeignKey(User)
#     aparcamiento = models.ForeignKey(Aparcamiento) #-->votos pueden ir a dif aparcamientos
