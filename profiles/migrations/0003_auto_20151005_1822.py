# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_internprofile_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internprofile',
            name='avatar',
        ),
        migrations.AddField(
            model_name='internprofile',
            name='_avatar',
            field=models.ImageField(null=True, upload_to=profiles.models._get_avatar_prefix, db_column=b'avatar', blank=True),
        ),
    ]
