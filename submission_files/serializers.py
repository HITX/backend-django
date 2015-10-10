from rest_framework.serializers import (
    CharField,
    FileField,
    URLField,
    ValidationError
)

from common.serializers import DynamicModelSerializer, ExpandableInfo

from submissions.models import Submission

from submission_files.models import SubmissionFile

class SubmissionFileSerializer(DynamicModelSerializer):
    filename = CharField(read_only=True)
    url = URLField(source='file_url', read_only=True)
    file = FileField(max_length=None, allow_empty_file=False, write_only=True)

    # TODO: make submission a non-required field (for detail put)
    # but add a check in create that requires it (for post)

    # TODO: override update() to auto set the updated date
    # (actually should have it call the manager's update method which
    # does the 'auto-setting')

    # TODO: need to ensure unique on owner/submission/filename somehow
    # possibly store filename in db and make unique constraint with it

    class Meta:
        model = SubmissionFile
        fields = (
            'id',
            'owner',
            'filename',
            'url',
            'submission',
            'created_date',
            'updated_date',
            'file'
        )
        read_only_fields = (
            'owner',
            'filename',
            'url',
            'created_date',
            'updated_date'
        )

    def create(self, validated_data):
        # User validation handled by DRY permissions
        user = self.context['request'].user

        # submission = Submission.objects.get(id=submission_id)
        submission = validated_data.pop('submission')
        if user != submission.submitter:
            raise PermissionDenied('You do not own this submission')

        return SubmissionFile.objects.create(
            validated_data,
            owner=user,
            submission=submission
        )
