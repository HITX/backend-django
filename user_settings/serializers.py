from rest_framework import serializers
from user_settings.models import UserSettings

class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ('data',)
