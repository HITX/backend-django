# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20151005_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgprofile',
            name='logo',
            field=models.ImageField(null=True, upload_to=profiles.models._get_logo_prefix, blank=True),
        ),
        migrations.AlterField(
            model_name='internprofile',
            name='avatar',
            field=models.ImageField(null=True, upload_to=profiles.models._get_avatar_prefix, blank=True),
        ),
    ]
