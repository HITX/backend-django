# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import mixins.models.permissions


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
            bases=(models.Model, mixins.models.permissions.IsAuthOrReadOnly),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=b'REGISTERED', choices=[(b'REGISTERED', b'Registered'), (b'SUBMITTED', b'Submitted'), (b'REJECTED', b'Rejected'), (b'ACCEPTED', b'Accepted')])),
                ('project', models.ForeignKey(to='projects.Project')),
                ('submitter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, mixins.models.permissions.IsAuth),
        ),
        migrations.AddField(
            model_name='project',
            name='submitters',
            field=models.ManyToManyField(related_name='submitted_projects', through='projects.Submission', to=settings.AUTH_USER_MODEL),
        ),
    ]
