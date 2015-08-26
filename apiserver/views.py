from django.contrib.auth.models import Group

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

from rest_framework import viewsets, permissions
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from apiserver.serializers import InternSerializer, OrgSerializer, GroupSerializer
from apiserver.models import User

# from user_settings.serializers import UserSettingsSerializer

from dry_rest_permissions.generics import DRYPermissions

class InternViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = InternSerializer
    permission_classes = [DRYPermissions,]

    def retrieve(self, request, pk=None):
        if pk == 'me':
            if not request.user.is_authenticated():
                raise AuthenticationFailed()
            if not request.user.is_intern:
                raise NotFound()
            return Response(InternSerializer(request.user).data)

        return super(InternViewSet, self).retrieve(request, pk)

class OrgViewSet(viewsets.ModelViewSet):
    queryset = User.objects.orgs
    serializer_class = OrgSerializer
    permission_classes = [DRYPermissions,]

    def retrieve(self, request, pk=None):
        if pk == 'me':
            if not request.user.is_authenticated():
                raise AuthenticationFailed()
            if not request.user.is_org:
                raise NotFound()
            return Response(OrgSerializer(request.user).data)

        return super(OrgViewSet, self).retrieve(request, pk)

    # @detail_route(methods=['get', 'post'])
    # def user_settings(self, requeset, pk=None):
    #     user = self.get_object()
    #
    #     if request.method == 'GET':
    #         return Response(UserSettingsSerializer(user.user_settings).data)
    #
    #     elif request.method == 'POST':
    #         serializer = UserSettingsSerializer(data=request.data)
    #
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    required_scopes = ['groups']
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
