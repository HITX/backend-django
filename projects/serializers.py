from rest_framework.serializers import IntegerField

from projects.models import Project

from apiserver.serializers import OrgSerializer

from common.serializers import DynamicModelSerializer, ExpandableInfo

class ProjectSerializer(DynamicModelSerializer):
    submission_count = IntegerField(source='submissions.count', required=False)

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
        read_only_fields = ('owner','submission_count')
        extra_kwargs = {
            'created_date': {'format': '%b %d'},
            'start_date': {'format': '%b %d'},
            'end_date': {'format': '%b %d'}
        }
