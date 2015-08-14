from django.db import models

class Profile(models.Model):
    user = models.OneToOneField('apiserver.User')
    data = models.CharField(max_length=256, default='profile data')
