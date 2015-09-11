from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from dry_rest_permissions.generics import DRYPermissions

from projects.models import Project
from projects.serializers import ProjectSerializer

from submissions.models import Submission
from submissions.serializers import SubmissionSerializer

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
