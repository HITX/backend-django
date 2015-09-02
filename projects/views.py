from rest_framework import status
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from dry_rest_permissions.generics import DRYPermissions

from projects.models import Project, Submission
from projects.serializers import ProjectSerializer, SubmissionSerializer

from common.constants import SubmissionStatus

from common.views import DynamicModelViewSet

class ProjectViewSet(DynamicModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [DRYPermissions,]

    def create(self, request):
        # TODO: change this to get_serializer
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def register(self, request, pk=None):
        submission = Submission.objects.create(request.user, self.get_object())
        return Response(SubmissionSerializer(submission).data)

class SubmissionViewSet(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        GenericViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [DRYPermissions,]

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
