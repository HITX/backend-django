# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apiserver.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
            managers=[
                ('objects', apiserver.models.UserManager()),
            ],
        ),
    ]