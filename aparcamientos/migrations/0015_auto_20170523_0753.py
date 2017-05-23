# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0014_auto_20170523_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamientos',
            name='numComentarios',
            field=models.IntegerField(default=0, blank=True),
        ),
    ]
