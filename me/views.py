from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from oauth2_provider.ext.rest_framework import TokenHasScope

from apiserver.exceptions import InvalidUserType

from me.serializers import MeSerializer
from apiserver.serializers import InternSerializer, OrgSerializer
from projects.serializers import ProjectSerializer, SubmissionSerializer

class MeViewSet(ViewSet):
    # Ignore DRY permissions as actions apply directly to user's own model
    required_scopes = ['read']
    permission_classes = [IsAuthenticated, TokenHasScope]

    def retrieve(self, request):
        serializer = MeSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def user(self, request):
        if request.user.is_intern:
            serializer = InternSerializer
        elif request.user.is_org:
            serializer = OrgSerializer
        else:
            raise Exception('Unknown user type')
        return Response(serializer(request.user, context={'request': request}).data)

    @detail_route(methods=['get'])
    def projects(self, request):
        if not request.user.is_org:
            raise InvalidUserType
        serializer = ProjectSerializer(request.user.projects, many=True, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def submissions(self, request):
        serializer = SubmissionSerializer(request.user.submissions, many=True, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['get'], url_path='settings')
    def user_settings(self, request):
        raise Exception('Not yet implemented')
