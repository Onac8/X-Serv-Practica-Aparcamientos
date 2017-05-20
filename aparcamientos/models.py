from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class Aparcamiento(models.Model):
# 	nombre = models.CharField(max_length=255, primary_key=True)
# 	direccion = models.TextField()
# 	creador = models.OneToOneField(Usuario)
#
#
# class Comentarios(models.Model):
# 	creador = models.ForeignKey(User)  para futuro Voto
#   aparcamiento = models.ForeignKey(Aparcamiento)
#   comentario = models.TextField()

# class Personal(models.model):
#   creador = models.OneToOneField(User)
#   titulo = models.CharField()     --> si no hay titulo: "Pagina de Usuario"

# class Voto(models.Model):
# 	creador = models.ForeignKey(User)
#   aparcamiento = models.ForeignKey(Aparcamiento) -->votos pueden ir a dif aparcamientos
#

# class ParkingSeleccion (models.Model):
#     Aparcamiento = models.ForeignKey(Aparcamientos)
#     Usuario = models.ForeignKey(User)
#     FichaPersonal = models.ForeignKey(PaginaPersonal)
#     Fecha = models.DateField(auto_now=True)
