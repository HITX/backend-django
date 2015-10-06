# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('submission_files', '0003_auto_20151004_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submissionfile',
            name='owner',
            field=models.ForeignKey(related_name='submitted_files', to=settings.AUTH_USER_MODEL),
        ),
    ]
