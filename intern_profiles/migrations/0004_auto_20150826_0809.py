# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('intern_profiles', '0003_auto_20150826_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internprofile',
            name='user',
            field=models.OneToOneField(related_name='internprofile', to=settings.AUTH_USER_MODEL),
        ),
    ]
