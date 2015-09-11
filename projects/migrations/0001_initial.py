# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import projects.models
import common.model_permissions
import django.utils.timezone
from django.conf import settings
import common.fields


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
                ('description', models.TextField(default=b'Project description', max_length=1024)),
                ('prize', common.fields.CurrencyField(default=1000)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(default=projects.models._default_end_date)),
                ('owner', models.ForeignKey(related_name='owned_projects', to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, common.model_permissions.IsAuthOrReadOnly),
        ),
    ]
