# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0012_auto_20170523_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamientos',
            name='numComentarios',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
