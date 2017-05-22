# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aparcamientos', '0006_auto_20170521_1713'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seleccionar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Fecha', models.DateField(auto_now=True)),
                ('Aparcamiento', models.ForeignKey(to='aparcamientos.Aparcamientos')),
                ('FichaPersonal', models.ForeignKey(to='aparcamientos.Personal')),
                ('Usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='contactosparking',
            name='Aparcamiento',
        ),
        migrations.RemoveField(
            model_name='parkingseleccion',
            name='Aparcamiento',
        ),
        migrations.RemoveField(
            model_name='parkingseleccion',
            name='FichaPersonal',
        ),
        migrations.RemoveField(
            model_name='parkingseleccion',
            name='Usuario',
        ),
        migrations.DeleteModel(
            name='ContactosParking',
        ),
        migrations.DeleteModel(
            name='ParkingSeleccion',
        ),
    ]
