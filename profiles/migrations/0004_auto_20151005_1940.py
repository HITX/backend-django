# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20151005_1822'),
    ]

    operations = [
        migrations.RenameField(
            model_name='internprofile',
            old_name='_avatar',
            new_name='avatar',
        ),
    ]
