from rest_framework.serializers import ModelSerializer, IntegerField, DateTimeField
from projects.models import Project, Submission

from apiserver.serializers import OrgSerializer

from common.serializers import DynamicModelSerializer, ExpandableFieldInfo

class ProjectSerializer(DynamicModelSerializer):
    submission_count = IntegerField(source='submissions.count')

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'description',
            'submission_count',
            'prize',
            'created_date',
            'start_date',
            'end_date'
        )
        expandable_fields = {
            'owner': ExpandableFieldInfo(
                serializer=OrgSerializer,
                kwargs={'read_only': True}
            )
        }
        read_only_fields = ('owner',)
        extra_kwargs = {
            'created_date': {'format': '%b %d'},
            'start_date': {'format': '%b %d'},
            'end_date': {'format': '%b %d'}
        }

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
