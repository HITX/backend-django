# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_submission_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='project',
            field=models.ForeignKey(related_name='submissions', to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='submitter',
            field=models.ForeignKey(related_name='intern_submissions', to=settings.AUTH_USER_MODEL),
        ),
    ]
