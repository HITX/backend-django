from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

from apiserver.models import User

from profiles.serializers import InternProfileSerializer, OrgProfileSerializer
from projects.serializers import SubmissionSerializer

class MeSerializer(ModelSerializer):
    submissions = SubmissionSerializer(many=True)
    profile = SerializerMethodField()
    # settings

    def get_profile(self, obj):
        user = self.context['request'].user
        if user.is_intern:
            serializer = InternProfileSerializer
        elif user.is_org:
            serializer = OrgProfileSerializer
        else:
            raise Exception('Unknown user type')

        return serializer(user.profile).data

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'user_type',
            'submissions',
            'profile'
        )
