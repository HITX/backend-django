from django.db import models
from django.conf import settings

from django.utils import timezone

from common.constants import UserTypes
from common.fields import CurrencyField
from common import model_permissions

def _default_end_date():
    return timezone.now() + timezone.timedelta(days=30)

class Project(models.Model, model_permissions.IsAuthOrReadOnly):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_projects')
    submitters = models.ManyToManyField(settings.AUTH_USER_MODEL, through='submissions.Submission', related_name='submitted_projects')
    title = models.CharField(max_length=256, default='Project Title')
    description = models.TextField(max_length=1024, default='Project description')
    prize = CurrencyField(default=1000)
    created_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=_default_end_date)

    # Class permissions
    @staticmethod
    def has_create_permission(request):
        return model_permissions.checkAuth(request, user_type=UserTypes.ORG, scopes=['write'])

    @staticmethod
    def has_register_permission(request):
        return model_permissions.checkAuth(request, user_type=UserTypes.INTERN, scopes=['write'])

    # Object permissions
    def has_object_read_permission(self, request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.owner

    def has_object_register_permission(self, request):
        return True

    def __str__(self):
        return self.title
