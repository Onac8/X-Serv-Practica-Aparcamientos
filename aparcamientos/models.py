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
    distrito = models.CharField(max_length=20)
    lat = models.FloatField()
    lon = models.FloatField()
    nComen = models.IntegerField()
    email = models.CharField(max_length=50, default="something")
    telefono = models.IntegerField()


class Comentario(models.Model):
    #creador = models.ForeignKey(User) --> para futuro voto
    aparcamiento = models.ForeignKey(Aparcamientos)
    texto = models.TextField()

class Personal(models.Model):
    creador = models.OneToOneField(User)
    titulo = models.CharField(max_length=60)

class Seleccionar (models.Model):
    Aparcamiento = models.ForeignKey(Aparcamientos)
    Usuario = models.ForeignKey(User)
    FichaPersonal = models.ForeignKey(Personal)
    Fecha = models.DateField(auto_now=True)


# class Voto(models.Model):
#     creador = models.ForeignKey(User)
#     aparcamiento = models.ForeignKey(Aparcamiento) #-->votos pueden ir a dif aparcamientos
