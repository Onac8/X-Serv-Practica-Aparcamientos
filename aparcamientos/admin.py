from django.contrib import admin

# Register your models here.
from aparcamientos.models import Aparcamientos
from aparcamientos.models import Comentario
from aparcamientos.models import Personal
from aparcamientos.models import Seleccionar


admin.site.register(Aparcamientos)
admin.site.register(Comentario)
admin.site.register(Personal)
admin.site.register(Seleccionar)
