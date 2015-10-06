from rest_framework import serializers
from profiles.models import InternProfile, OrgProfile

class InternProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.URLField(source='avatar_url_or_default', read_only=True)

    class Meta:
        model = InternProfile
        fields = ('first_name', 'last_name', 'avatar_url')

class OrgProfileSerializer(serializers.ModelSerializer):
    logo_url = serializers.URLField(source='logo_url_or_default', read_only=True)

    class Meta:
        model = OrgProfile
        fields = ('org_name', 'logo_url')
