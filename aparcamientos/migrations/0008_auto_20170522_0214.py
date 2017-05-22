# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0007_auto_20170522_0213'),
    ]

    operations = [
        migrations.AddField(
            model_name='aparcamientos',
            name='email',
            field=models.CharField(default=b'something', max_length=50),
        ),
        migrations.AddField(
            model_name='aparcamientos',
            name='telefono',
            field=models.IntegerField(default=910000000),
            preserve_default=False,
        ),
    ]
