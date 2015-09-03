# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internprofile',
            name='first_name',
            field=models.CharField(default=b'Thomas', max_length=50),
        ),
        migrations.AlterField(
            model_name='internprofile',
            name='last_name',
            field=models.CharField(default=b'Anderson', max_length=50),
        ),
        migrations.AlterField(
            model_name='orgprofile',
            name='org_name',
            field=models.CharField(default=b'Initech Inc.', max_length=50),
        ),
    ]
