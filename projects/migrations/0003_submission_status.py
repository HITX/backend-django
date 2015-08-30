# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_remove_submission_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='status',
            field=models.CharField(default=b'REGISTERED', max_length=20, choices=[(b'REGISTERED', b'Registered'), (b'SUBMITTED', b'Submitted'), (b'REJECTED', b'Rejected'), (b'ACCEPTED', b'Accepted')]),
        ),
    ]
