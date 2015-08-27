from django.contrib.auth.models import Group

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from apiserver.serializers import InternSerializer, OrgSerializer, GroupSerializer
from apiserver.models import User

# from user_settings.serializers import UserSettingsSerializer

from dry_rest_permissions.generics import DRYPermissions

class InternViewSet(ModelViewSet):
    queryset = User.objects.interns
    serializer_class = InternSerializer
    permission_classes = [DRYPermissions,]

class OrgViewSet(ModelViewSet):
    queryset = User.objects.orgs
    serializer_class = OrgSerializer
    permission_classes = [DRYPermissions,]

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

class MeViewSet(ViewSet):
    required_scopes = ['read']
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]

    def retrieve(self, request):
        if request.user.is_intern:
            serializer = InternSerializer
        elif request.user.is_org:
            serializer = OrgSerializer
        else:
            raise Exception('Unknown user type')

        return Response(serializer(request.user).data)

    def update(self, request):
        raise Exception('Not yet implemented')

    def partial_update(self, request):
        raise Exception('Not yet implemented')

    def destroy(self, request):
        raise Exception('Not yet implemented')

    @detail_route(methods=['get', 'post'], url_path='settings')
    def user_settings(self, request):
        raise Exception('Not yet implemented')


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    required_scopes = ['groups']
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
