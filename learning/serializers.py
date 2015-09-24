from rest_framework.serializers import ModelSerializer
from learning.models import Learn

class LearnSerializer(ModelSerializer):
    class Meta:
        model = Learn
        fields = (
            'name',
            'type',
            'bullshit'
        )
