from apiserver.models import User
from projects.models import Project

from profiles.serializers import InternProfileSerializer, OrgProfileSerializer
from projects.serializers import SubmissionSerializer, ProjectSerializer

from common.serializers import MeDynamicModelSerializer, ExpandableInfo
from common.exceptions import InvalidUserType, InternalUserTypeError

from rest_framework.serializers import PrimaryKeyRelatedField, SerializerMethodField

class MeSerializer(MeDynamicModelSerializer):
    submissions = PrimaryKeyRelatedField(many=True, read_only=True)
    projects = SerializerMethodField()
    # settings

    def get_projects(self, obj):
        user = self.context['request'].user
        if user.is_intern:
            return None
        elif user.is_org:
            return user.projects.values_list('id', flat=True).order_by('id')
        else:
            raise InternalUserTypeError

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

            # Disallow interns from expanding projects
            # raise ExpandException('Expand not available for fields: projects')

        elif user.is_org:
            serializer = OrgProfileSerializer

            # self.Meta.expandable_fields['projects'] = ExpandableInfo(ProjectSerializer, many=True)

        else:
            raise Exception('Unknown user type')

        setattr(self.Meta, 'inline_fields', {'profile': serializer})

        super(MeSerializer, self).__init__(*args, **kwargs)

        # print self.fields
