# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_remove_submission_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, b'Registered'), (2, b'Submitted'), (3, b'Rejected'), (4, b'Accepted')]),
        ),
    ]
