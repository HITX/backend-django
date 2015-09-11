# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import common.model_permissions


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=1, choices=[(1, b'Registered'), (2, b'Submitted'), (3, b'Rejected'), (4, b'Accepted')])),
                ('project', models.ForeignKey(related_name='submissions', to='projects.Project')),
                ('submitter', models.ForeignKey(related_name='intern_submissions', to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, common.model_permissions.IsAuth),
        ),
    ]
