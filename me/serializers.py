from apiserver.models import User

from profiles.serializers import InternProfileSerializer, OrgProfileSerializer
from projects.serializers import SubmissionSerializer

from common.serializers import DynamicModelSerializer, ExpandableInfo
from common.exceptions import InvalidUserType

from rest_framework.serializers import PrimaryKeyRelatedField

class MeSerializer(DynamicModelSerializer):
    submissions = PrimaryKeyRelatedField(many=True, read_only=True)
    # settings

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'user_type',
        )
        expandable_fields = {
            'submissions': ExpandableInfo(SubmissionSerializer, many=True)
                # serializer=SubmissionSerializer,
                # kwargs={'many': True}
            # )
        }

    def __init__(self, *args, **kwargs):
        # Need to update fields before super(), must use raw context from
        # kwargs, not self.context() helper
        user = kwargs['context']['request'].user
        if user.is_intern:
            serializer = InternProfileSerializer
        elif user.is_org:
            serializer = OrgProfileSerializer
        else:
            raise Exception('Unknown user type')

        setattr(self.Meta, 'inline_fields', {'profile': serializer})

        super(MeSerializer, self).__init__(*args, **kwargs)
