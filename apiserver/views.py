from django.contrib.auth.models import Group

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

from rest_framework import viewsets, permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from apiserver.serializers import UserSerializer, GroupSerializer
from apiserver.models import User

from dry_rest_permissions.generics import DRYPermissions

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [DRYPermissions,]

    def retrieve(self, request, pk=None):
        if pk == 'me':
            print('In the me retrieve section')
            print(request.user)
            if not request.user.is_authenticated():
                raise AuthenticationFailed()
            return Response(UserSerializer(request.user).data)

        return super(UserViewSet, self).retrieve(request, pk)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    required_scopes = ['groups']
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
