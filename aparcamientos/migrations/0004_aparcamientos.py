# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0003_delete_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aparcamientos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=70)),
                ('descripcion', models.TextField()),
                ('urlP', models.URLField()),
                ('accesibilidad', models.BooleanField()),
                ('direccion', models.CharField(max_length=60)),
                ('barrio', models.CharField(max_length=20)),
                ('distrito', models.CharField(max_length=20)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('nComen', models.IntegerField()),
            ],
        ),
    ]
