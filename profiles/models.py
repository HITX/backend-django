from django.db import models

from django.conf import settings

class InternProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name = 'intern_profile')
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'intern_profile'

class OrgProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name = 'org_profile')
    org_name = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'org_profile';
