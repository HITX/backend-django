from rest_framework.serializers import ModelSerializer
from projects.models import Project, Submission

# from apiserver.serializers import OrgSerializer

class ProjectSerializer(ModelSerializer):
    # owner = OrgSerializer(required=False)

    class Meta:
        model = Project
        fields = (
            'id',
            'owner',
            'title',
            'description'
        )
        read_only_fields = ('owner',)

    def __init__(self, *args, **kwargs):
        expand = kwargs.pop('expand', None)
        print expand
        super(ProjectSerializer, self).__init__(*args, **kwargs)

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
