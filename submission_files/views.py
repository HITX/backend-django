from django.conf import settings

import boto
from boto.s3.key import Key

from rest_framework.serializers import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser

from dry_rest_permissions.generics import DRYPermissions

from submissions.models import Submission

from submission_files.models import SubmissionFile
from submission_files.serializers import SubmissionFileSerializer

from common.views import DynamicModelViewSet

class SubmissionFileViewSet(DynamicModelViewSet):
    serializer_class = SubmissionFileSerializer
    permission_classes = [DRYPermissions,]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        # DRY permissions enforce that user is not anonymous
        queryset = self.request.user.submission_files

        submission_id = self.request.query_params.get('submission', None)
        if submission_id:
            queryset = queryset.filter(submission__id=submission_id)

        return queryset

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.file.delete(save=False)
        return super(SubmissionFileViewSet, self).destroy(request, pk)
