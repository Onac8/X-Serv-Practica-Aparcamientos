# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0005_auto_20170520_1916'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aparcamientos',
            old_name='urlP',
            new_name='url',
        ),
        migrations.AlterField(
            model_name='aparcamientos',
            name='accesibilidad',
            field=models.IntegerField(),
        ),
    ]
