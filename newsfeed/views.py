# from oauth2_provider.ext.rest_framework import TokenHasScope

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from projects.models import Project
from projects.serializers import ProjectSerializer

class NewsfeedViewSet(GenericViewSet):
    # order_by(-created_date)
    queryset = Project.objects.all()
    required_scopes = ['read']
    permission_classes = []

    def retrieve(self, request):
        serializer = ProjectSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)
