from rest_framework import serializers
from profiles.models import InternProfile, OrgProfile

class InternProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternProfile
        fields = ('first_name', 'last_name')

class OrgProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgProfile
        fields = ('org_name',)
