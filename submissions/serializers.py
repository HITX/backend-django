from rest_framework.serializers import PrimaryKeyRelatedField

from apiserver.serializers import InternSerializer

from projects.serializers import ProjectSerializer

from submissions.models import Submission

from common.serializers import DynamicModelSerializer, ExpandableInfo

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
