from django.db import models
from django.utils import timezone
from django.conf import settings

from custom_storages import PrivateMediaStorage

from rest_framework.serializers import ValidationError

from common import model_permissions
from common.constants import UserTypes

from submissions.models import Submission

class SubmissionFileManager(models.Manager):
    def create(self, validated_data, owner, submission, commit=True):
        prefix = '/'.join((str(submission.id), str(owner.id)))
        validated_data['prefix'] = prefix

        submission_file = SubmissionFile(**validated_data)
        submission_file.owner = owner
        submission_file.submission = submission

        if commit:
            submission_file.save()
        return submission_file


def _get_file_prefix(instance, filename):
    if not instance.prefix:
        raise ValidationError('Missing \'prefix\'')
    return '/'.join(('submissions', instance.prefix, filename))


class SubmissionFile(models.Model, model_permissions.IsAuth):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='submitted_files')
    submission = models.ForeignKey(Submission, related_name='files')
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    file = models.FileField(
        storage=PrivateMediaStorage(),
        upload_to=_get_file_prefix
    )

    objects = SubmissionFileManager()

    def _get_s3_key(self):
        return self.file.name
    s3_key = property(_get_s3_key)

    # TODO: make another property for filename that splits self.file.name
    # probably use it in serializer
    # Potentially add more props for things that can be gleaned from self.file like size?

    def __init__(self, *args, **kwargs):
        prefix = kwargs.pop('prefix', None)
        self.prefix = prefix
        super(SubmissionFile, self).__init__(*args, **kwargs)

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
        return (
            request.user == self.owner or
            request.user == self.submission.project.owner
        )


        # submission = self.submission
        # return (
        #     (request.user == submission.submitter) or
        #     (request.user == submission.project.owner)
        # )

    def has_object_write_permission(self, request):
        return request.user == self.owner
