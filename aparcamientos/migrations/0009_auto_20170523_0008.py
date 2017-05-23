# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0008_auto_20170522_0214'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aparcamientos',
            old_name='lat',
            new_name='latitud',
        ),
        migrations.RenameField(
            model_name='aparcamientos',
            old_name='lon',
            new_name='longitud',
        ),
        migrations.RenameField(
            model_name='aparcamientos',
            old_name='nComen',
            new_name='numComentarios',
        ),
    ]
