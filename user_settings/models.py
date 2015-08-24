from django.db import models

class UserSettings(models.Model):
    user = models.OneToOneField('apiserver.User')
    data = models.CharField(max_length=256, default='settings data')

    
