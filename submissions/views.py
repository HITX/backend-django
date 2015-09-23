from django.conf import settings

from rest_framework.decorators import detail_route
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ValidationError

from dry_rest_permissions.generics import DRYPermissions

from submissions.models import Submission
from submissions.serializers import SubmissionSerializer

from common.constants import SubmissionStatus, S3MediaDirs
from common.views import DynamicModelViewSet

from boto3 import client

class SubmissionViewSet(DynamicModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [DRYPermissions,]

    def list(self, request):
        submissions = request.user.submissions
        return Response(SubmissionSerializer(submissions, many=True).data);

    def _update_status(self, new_status):
        submission = self.get_object()
        submission.status = new_status
        submission.save()
        return Response(SubmissionSerializer(submission).data)

    @detail_route(methods=['post'])
    def submit(self, request, pk=None):
        return self._update_status(SubmissionStatus.SUBMITTED)

    @detail_route(methods=['post'])
    def accept(self, request, pk=None):
        return self._update_status(SubmissionStatus.ACCEPTED)

    @detail_route(methods=['post'])
    def reject(self, request, pk=None):
        return self._update_status(SubmissionStatus.REJECTED)

    @detail_route(methods=['get', 'post'])
    def files(self, request, pk=None):
        submission = self.get_object()

        if request.method == 'GET':
            client_method = 'get_object'
            filename = request.query_params.get('filename', None)
            http_method = 'GET'
        else:
            if request.user != submission.submitter:
                raise PermissionDenied
            client_method = 'put_object'
            filename = request.data.get('filename', None)
            content_type = request.data.get('content-type', None)
            http_method = 'PUT'

        if not filename:
            raise ValidationError('filename is required')

        if not content_type:
            # content_type = 'application/octet-stream'
            content_type = 'text/plain;charset=utf-8'
            # content_type = 'application/json; charset=utf-8'

        s3_client = client('s3')
        key_string = '/'.join((
            S3MediaDirs.SUBMISSIONS,
            str(submission.id),
            str(request.user.id),
            filename
        ))

        # key_string = filename

        presigned_url = s3_client.generate_presigned_url(
            client_method,
            Params={
                'Bucket': settings.AWS_S3_BUCKET,
                'Key': key_string,
                'ContentType': content_type
            },
            HttpMethod=http_method
        )

        return Response({'url': presigned_url})
