from rest_framework.decorators import detail_route
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from dry_rest_permissions.generics import DRYPermissions

from submissions.models import Submission
from submissions.serializers import SubmissionSerializer

from common.constants import SubmissionStatus
from common.views import DynamicModelViewSet

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
