from rest_framework.serializers import ModelSerializer
from projects.models import Project, Submission

from apiserver.serializers import OrgSerializer

from common.serializers import DynamicModelSerializer, ExpandableFieldInfo

class ProjectSerializer(DynamicModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'description'
        )
        expandable_fields = {
            'owner': ExpandableFieldInfo(
                serializer=OrgSerializer,
                kwargs={'read_only': True}
            )
        }
        read_only_fields = ('owner',)

class SubmissionSerializer(ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Submission
        fields = (
            'id',
            'submitter',
            'status',
            'project'
        )
