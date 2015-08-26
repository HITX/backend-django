from rest_framework import serializers
from org_profiles.models import OrgProfile

class OrgProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgProfile
        fields = ('data',)
