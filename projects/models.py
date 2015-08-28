from django.db import models

from django.conf import settings

class Project(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=256, default='Project Title')
    description = models.TextField(max_length=1024, default='Project description and so on...')

    @staticmethod
    def has_read_permission(request):
        return True

    @staticmethod
    def has_write_permission(request):
        """
        Must be authenticated as an organization and token must
        have write scope.
        """

        user = request.user
        token = request.auth

        if (user and token and
            user.is_authenticated() and
            token.is_valid(['write']) and
            user.is_org):
            return True

        return False

    def has_object_read_permission(self, request):
        return True

    def has_object_write_permission(self, request):
        """
        Must be owner of project
        """
        return request.user == self.owner
