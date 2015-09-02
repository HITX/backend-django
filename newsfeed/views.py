from rest_framework.response import Response

from common.views import DynamicGenericViewSet

from projects.models import Project
from projects.serializers import ProjectSerializer

class NewsfeedViewSet(DynamicGenericViewSet):
    # order_by(-created_date)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    required_scopes = ['read']
    permission_classes = []

    def retrieve(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
