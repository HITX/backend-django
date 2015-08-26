from rest_framework import serializers
from intern_profiles.models import InternProfile

class InternProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternProfile
        fields = ('data',)
