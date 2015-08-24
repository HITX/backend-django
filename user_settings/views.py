from django.contrib.auth.decorators import login_required

from rest_framework import views
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated

from user_settings.models import UserSettings
from user_settings.serializers import UserSettingsSerializer

class UserSettingsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        settings = request.user.usersettings
        serializer = UserSettingsSerializer(settings)
        return Response(serializer.data)

    def post(self, request, format=None):
        if request.auth.is_valid(['write']):
            settings = request.user.usersettings
            serializer = UserSettingsSerializer(settings, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serailizer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise AuthenticationFailed()
