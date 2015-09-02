from rest_framework.serializers import ModelSerializer
from projects.models import Project, Submission

from apiserver.serializers import OrgSerializer

from common.serializers import ExpandableModelSerializer

class ProjectSerializer(ExpandableModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'description'
        )
        expandable_fields = {'owner': OrgSerializer}
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
