# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intern_profiles', '0002_auto_20150826_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internprofile',
            name='data',
            field=models.CharField(default=b'intern profile data', max_length=256),
        ),
    ]
