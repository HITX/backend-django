# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import projects.models
import django.utils.timezone
import common.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='end_date',
            field=models.DateTimeField(default=projects.models._default_end_date),
        ),
        migrations.AddField(
            model_name='project',
            name='prize',
            field=common.fields.CurrencyField(default=1000),
        ),
        migrations.AddField(
            model_name='project',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(default=b'Project description', max_length=1024),
        ),
    ]
