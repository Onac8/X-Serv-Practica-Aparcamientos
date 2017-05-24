# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0015_auto_20170523_0753'),
    ]

    operations = [
        migrations.AddField(
            model_name='personal',
            name='color',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='personal',
            name='letra',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
