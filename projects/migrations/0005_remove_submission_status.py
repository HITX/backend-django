# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20150830_0408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='status',
        ),
    ]
