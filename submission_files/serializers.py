from common.serializers import DynamicModelSerializer, ExpandableInfo

from submission_files.models import SubmissionFile

class SubmissionFileSerializer(DynamicModelSerializer):

    class Meta:
        model = SubmissionFile
        fields = (
            'id',
            'submission',
            'filename',
            'size',
            'created_date',
            'updated_date'
        )
