# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0002_auto_20170519_0541'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
