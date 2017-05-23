# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0010_auto_20170523_0712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamientos',
            name='distrito',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='aparcamientos',
            name='latitud',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='aparcamientos',
            name='longitud',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='aparcamientos',
            name='telefono',
            field=models.CharField(default=b'S/T', max_length=40),
        ),
    ]
