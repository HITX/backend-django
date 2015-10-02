from django.db import models
from django.utils import timezone

from common import model_permissions
from common.constants import UserTypes

from submissions.models import Submission

class SubmissionFile(models.Model, model_permissions.IsAuth):
    submission = models.ForeignKey(Submission, related_name='files')
    filename = models.CharField(max_length=256)
    size = models.PositiveIntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    bucket_key = models.CharField(max_length=256)

    @staticmethod
    def has_write_permission(request):
        return (
            model_permissions.checkAuth(
                request,
                user_type=UserTypes.INTERN,
                scopes=['write']
            )
        )

    def has_object_read_permission(self, request):
        submission = self.submission
        return (
            (request.user == submission.submitter) or
            (request.user == submission.project.owner)
        )
