from django.db import models

from django.conf import settings



def _get_avatar_prefix(instance, filename):
    return '/'.join(('avatars', instance.id))

class InternProfile(models.Model):
    DEFAULT_AVATAR_URL = settings.STATIC_URL + 'avatars/default.jpg'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name = 'intern_profile')
    first_name = models.CharField(max_length=50, default='Thomas')
    last_name = models.CharField(max_length=50, default='Anderson')
    avatar = models.ImageField(
        upload_to=_get_avatar_prefix,
        null=True,
        blank=True
    )

    def _get_avatar_url_or_default(self):
        if self.avatar:
            return self.avatar.url
        return self.DEFAULT_AVATAR_URL
    avatar_url_or_default = property(_get_avatar_url_or_default)

    class Meta:
        db_table = 'intern_profile'


def _get_logo_prefix(instance, filename):
    return '/'.join(('logos', instance.id))

class OrgProfile(models.Model):
    DEFAULT_LOGO_URL = settings.STATIC_URL + 'logos/default.jpg'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name = 'org_profile')
    org_name = models.CharField(max_length=50, default='Initech Inc.')
    logo = models.ImageField(
        upload_to=_get_logo_prefix,
        null=True,
        blank=True
    )

    def _get_logo_url_or_default(self):
        if self.logo:
            return self.logo.url
        return self.DEFAULT_LOGO_URL
    logo_url_or_default = property(_get_logo_url_or_default)

    class Meta:
        db_table = 'org_profile';
