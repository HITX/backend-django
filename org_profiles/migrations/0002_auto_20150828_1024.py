# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('org_profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgprofile',
            name='user',
            field=models.OneToOneField(related_name='org_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelTable(
            name='orgprofile',
            table='org_profile',
        ),
    ]
