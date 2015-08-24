from django.contrib.auth.models import Group
from rest_framework import serializers
from apiserver.models import User
from profiles.serializers import ProfileSerializer

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'profile',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create(validated_data)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
