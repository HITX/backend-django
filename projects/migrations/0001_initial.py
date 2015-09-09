# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import common.model_permissions


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'Project Title', max_length=256)),
                ('description', models.TextField(default=b'Project description and so on...', max_length=1024)),
                ('owner', models.ForeignKey(related_name='owned_projects', to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, common.model_permissions.IsAuthOrReadOnly),
        ),
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
        migrations.AddField(
            model_name='project',
            name='submitters',
            field=models.ManyToManyField(related_name='submitted_projects', through='projects.Submission', to=settings.AUTH_USER_MODEL),
        ),
    ]
