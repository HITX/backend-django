from django.conf import settings
if settings.DEBUG:
    from common.view_permissions import DebugTokenHasScope as TokenHasScope
else:
    from oauth2_provider.ext.rest_framework import TokenHasScope

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from common.exceptions import InvalidUserType
from common.views import DynamicGenericViewSet

from me.serializers import MeSerializer
from apiserver.serializers import InternSerializer, OrgSerializer
from projects.serializers import ProjectSerializer
from submissions.serializers import SubmissionSerializer

class MeViewSet(DynamicGenericViewSet):
    # Ignore DRY permissions as actions apply directly to user's own model
    serializer_class = MeSerializer
    required_scopes = ['read']
    permission_classes = [IsAuthenticated, TokenHasScope]

    def retrieve(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
