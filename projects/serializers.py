from rest_framework.serializers import ModelSerializer
from projects.models import Project, Submission

class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id',
            'owner',
            'title',
            'description'
        )
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
