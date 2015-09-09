from django.conf import settings
if settings.DEBUG:
    from common.view_permissions import DebugTokenHasScope as TokenHasScope
else:
    from oauth2_provider.ext.rest_framework import TokenHasScope

from django.contrib.auth.models import Group

from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import AuthenticationFailed, NotFound

from apiserver.serializers import InternSerializer, OrgSerializer, GroupSerializer
from apiserver.models import User

from dry_rest_permissions.generics import DRYPermissions

from common.views import DynamicModelViewSet

class InternViewSet(DynamicModelViewSet):
    queryset = User.objects.interns
    serializer_class = InternSerializer
    permission_classes = [DRYPermissions,]

class OrgViewSet(DynamicModelViewSet):
    queryset = User.objects.orgs
    serializer_class = OrgSerializer
    permission_classes = [DRYPermissions,]

class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    # Use normal permissions for third party model
    required_scopes = ['groups']
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
