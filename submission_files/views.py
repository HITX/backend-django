from rest_framework.serializers import ValidationError

from dry_rest_permissions.generics import DRYPermissions

from submissions.models import Submission

from submission_files.models import SubmissionFile
from submission_files.serializers import SubmissionFileSerializer

from common.views import DynamicModelViewSet

class SubmissionFileViewSet(DynamicModelViewSet):
    serializer_class = SubmissionFileSerializer
    permission_classes = [DRYPermissions,]

    def get_queryset(self):
        submission_id = self.request.query_params.get('submission', None)
        if not submission_id:
            raise ValidationError('query parameter \'submission\' required')

        return SubmissionFile.objects.filter(submission=submission_id)
