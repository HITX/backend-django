# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import submission_files.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('submissions', '0001_initial'),
        ('submission_files', '0002_auto_20151004_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissionfile',
            name='owner',
            field=models.ForeignKey(related_name='submission_files', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submissionfile',
            name='submission',
            field=models.ForeignKey(related_name='files', default=2, to='submissions.Submission'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='submissionfile',
            name='file',
            field=models.FileField(upload_to=submission_files.models._get_file_prefix),
        ),
    ]
