# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('nombre', models.CharField(default=b'', max_length=100, serialize=False, primary_key=True)),
            ],
        ),
    ]
