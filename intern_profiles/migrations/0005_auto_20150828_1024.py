# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('intern_profiles', '0004_auto_20150826_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internprofile',
            name='user',
            field=models.OneToOneField(related_name='intern_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelTable(
            name='internprofile',
            table='intern_profile',
        ),
    ]
