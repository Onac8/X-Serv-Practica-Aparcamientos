# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0013_auto_20170523_0733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamientos',
            name='email',
            field=models.CharField(default=b'No E-Mail', max_length=50),
        ),
        migrations.AlterField(
            model_name='aparcamientos',
            name='telefono',
            field=models.CharField(default=b'No Tlf', max_length=40),
        ),
    ]
