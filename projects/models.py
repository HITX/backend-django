from django.db import models

class Project(models.Model):
    field_1 = models.CharField(max_length=100, default='default')
    field_2 = models.CharField(max_length=100, default='default')
    field_3 = models.CharField(max_length=100, default='default')
    owner = models.ForeignKey('auth.User', related_name='projects')
