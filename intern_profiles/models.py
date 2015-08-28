from django.db import models

from django.conf import settings

class InternProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name = 'intern_profile')
    data = models.CharField(max_length=256, default='intern profile data')

    class Meta:
        db_table = 'intern_profile'
