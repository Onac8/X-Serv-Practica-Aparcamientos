# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='password',
            field=models.CharField(default=b'', max_length=32),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(default=b'', max_length=32, serialize=False, primary_key=True),
        ),
    ]
