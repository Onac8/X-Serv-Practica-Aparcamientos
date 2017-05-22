# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aparcamientos', '0004_aparcamientos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.TextField()),
                ('aparcamiento', models.ForeignKey(to='aparcamientos.Aparcamientos')),
            ],
        ),
        migrations.CreateModel(
            name='ContactosParking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('telefono', models.IntegerField()),
                ('email', models.CharField(max_length=32)),
                ('Aparcamiento', models.ForeignKey(to='aparcamientos.Aparcamientos')),
            ],
        ),
        migrations.CreateModel(
            name='ParkingSeleccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Fecha', models.DateField(auto_now=True)),
                ('Aparcamiento', models.ForeignKey(to='aparcamientos.Aparcamientos')),
            ],
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=60)),
                ('creador', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='parkingseleccion',
            name='FichaPersonal',
            field=models.ForeignKey(to='aparcamientos.Personal'),
        ),
        migrations.AddField(
            model_name='parkingseleccion',
            name='Usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
