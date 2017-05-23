# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0009_auto_20170523_0008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seleccionar',
            old_name='Aparcamiento',
            new_name='aparcamiento',
        ),
        migrations.RenameField(
            model_name='seleccionar',
            old_name='Fecha',
            new_name='fecha',
        ),
        migrations.RenameField(
            model_name='seleccionar',
            old_name='FichaPersonal',
            new_name='fichaPersonal',
        ),
        migrations.RenameField(
            model_name='seleccionar',
            old_name='Usuario',
            new_name='usuario',
        ),
    ]
