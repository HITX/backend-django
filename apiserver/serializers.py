from django.contrib.auth.models import Group
from rest_framework import serializers
from apiserver.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
