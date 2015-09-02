# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InternProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50, blank=True)),
                ('last_name', models.CharField(max_length=50, blank=True)),
                ('user', models.OneToOneField(related_name='intern_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'intern_profile',
            },
        ),
        migrations.CreateModel(
            name='OrgProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('org_name', models.CharField(max_length=50, blank=True)),
                ('user', models.OneToOneField(related_name='org_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'org_profile',
            },
        ),
    ]
