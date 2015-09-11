from apiserver.models import User
from projects.models import Project

from profiles.serializers import InternProfileSerializer, OrgProfileSerializer
from projects.serializers import ProjectSerializer
from submissions.serializers import SubmissionSerializer

from common.serializers import DynamicModelSerializer, ExpandableInfo
from common.exceptions import InvalidUserType, InternalUserTypeError

from rest_framework.serializers import PrimaryKeyRelatedField, SerializerMethodField

class MeSerializer(DynamicModelSerializer):
    submissions = PrimaryKeyRelatedField(many=True, read_only=True)
    projects = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'user_type',
            'submissions',
            'projects'
        )
        expandable_fields = {
            'submissions': ExpandableInfo(SubmissionSerializer, many=True),
            'projects': ExpandableInfo(ProjectSerializer, many=True)
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

        # Add appropriate profile given user type
        setattr(self.Meta, 'inline_fields', {'profile': serializer})

        super(MeSerializer, self).__init__(*args, **kwargs)

        # Remove projects from response for interns
        # and submissions for response for orgs
        if user.is_intern:
            self.fields.pop('projects')
        elif user.is_org:
            self.fields.pop('submissions')
