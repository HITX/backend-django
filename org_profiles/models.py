from django.db import models

from django.conf import settings

class OrgProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name = 'orgprofile')
    data = models.CharField(max_length=256, default='org profile data')