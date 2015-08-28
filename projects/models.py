from django.db import models
from django.conf import settings

from apiserver.models import User

from mixins.models.permissions import IsAuthenticatedOrReadOnlyAndCreate

class Project(models.Model, IsAuthenticatedOrReadOnlyAndCreate):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=256, default='Project Title')
    description = models.TextField(max_length=1024, default='Project description and so on...')

    # Permitted user type for authentication mixin
    auth_user_type = User.USER_TYPE_ORG

    # Object permissions
    def has_object_read_permission(self, request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.owner
