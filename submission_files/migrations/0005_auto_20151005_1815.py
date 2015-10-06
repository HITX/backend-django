# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import submission_files.models
import custom_storages


class Migration(migrations.Migration):

    dependencies = [
        ('submission_files', '0004_auto_20151005_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submissionfile',
            name='file',
            field=models.FileField(storage=custom_storages.PrivateMediaStorage(), upload_to=submission_files.models._get_file_prefix),
        ),
    ]
