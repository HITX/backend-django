from django.conf import settings
if settings.DEBUG:
    from common.view_permissions import DebugTokenHasScope as TokenHasScope
else:
    from oauth2_provider.ext.rest_framework import TokenHasScope

from django.contrib.auth.models import Group

from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.exceptions import AuthenticationFailed, NotFound

from apiserver.serializers import (
    # EmailSerializer,
    # PasswordSerializer,
    InternSerializer,
    OrgSerializer,
    GroupSerializer
)
from apiserver.models import User

from profiles.serializers import InternProfileSerializer

from dry_rest_permissions.generics import DRYPermissions

from common.views import DynamicModelViewSet

# TODO: Remove this
from rest_framework.serializers import ValidationError

class InternViewSet(DynamicModelViewSet):
    queryset = User.objects.interns
    serializer_class = InternSerializer
    permission_classes = [DRYPermissions,]

    # Override update to use profile serializer
    # def update(self, request, *args, **kwargs):
    #     print 'Made it to update'
    #     partial = kwargs.pop('partial', False)
    #
    #     profile_instance = self.get_object().profile
    #     serializer = InternProfileSerializer(
    #         profile_instance,
    #         data=request.data,
    #         partial=partial
    #     )
    #
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)

    # @detail_route(methods=['post'], url_path='set-password')
    # def set_password(self, request, pk=None):
    #     serializer = PasswordSerializer(data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         user.set_password(serializer.data['password'])
    #         user.save()
    #         return Response({'status': 'password set'})
    #     else:
    #         return Response(serializer.errors)
    #
    # @detail_route(methods=['post'], url_path='set-email')
    # def set_email(self, request, pk=None):
    #     serializer = EmailSerializer(data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         user.set_email(serializer.data['email'])
    #         user.save()
    #         return Response({'status': 'email set'})
    #     else:
    #         return Response(serializer.errors)



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
