# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission_files', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submissionfile',
            name='bucket_key',
        ),
        migrations.RemoveField(
            model_name='submissionfile',
            name='filename',
        ),
        migrations.RemoveField(
            model_name='submissionfile',
            name='size',
        ),
        migrations.RemoveField(
            model_name='submissionfile',
            name='submission',
        ),
        migrations.AddField(
            model_name='submissionfile',
            name='file',
            field=models.FileField(default='blah', upload_to=b'submissions'),
            preserve_default=False,
        ),
    ]
