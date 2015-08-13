from rest_framework import serializers
from django.contrib.auth.models import User
from projects.models import Project

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Project
        fields = ('url', 'field_1', 'field_2', 'field_3', 'owner')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())

    class Meta:
        model = User
        fields = ('url', 'username', 'projects')
