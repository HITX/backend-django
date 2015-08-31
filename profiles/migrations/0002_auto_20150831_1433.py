# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internprofile',
            name='data',
        ),
        migrations.RemoveField(
            model_name='orgprofile',
            name='data',
        ),
        migrations.AddField(
            model_name='internprofile',
            name='first_name',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='internprofile',
            name='last_name',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='orgprofile',
            name='org_name',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
