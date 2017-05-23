# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0011_auto_20170523_0731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamientos',
            name='numComentarios',
            field=models.IntegerField(blank=True),
        ),
    ]
