from rest_framework.serializers import ModelSerializer, IntegerField, DateTimeField, PrimaryKeyRelatedField
from projects.models import Project, Submission

from apiserver.serializers import InternSerializer, OrgSerializer

from common.serializers import DynamicModelSerializer, ExpandableInfo

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
            'end_date',
            'owner'
        )
        expandable_fields = {
            'owner': ExpandableInfo(OrgSerializer, read_only=True)
        }
        read_only_fields = ('owner',)
        extra_kwargs = {
            'created_date': {'format': '%b %d'},
            'start_date': {'format': '%b %d'},
            'end_date': {'format': '%b %d'}
        }

class SubmissionSerializer(DynamicModelSerializer):
    project = PrimaryKeyRelatedField(read_only=True)
    submitter = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Submission
        fields = (
            'id',
            'status',
            'project',
            'submitter'
        )
        expandable_fields = {
            'project': ExpandableInfo(ProjectSerializer),
            'submitter': ExpandableInfo(InternSerializer)
        }
