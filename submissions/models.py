from django.db import models
from django.conf import settings

from common.constants import UserTypes, SubmissionStatus

from common import model_permissions

from projects.models import Project

class SubmissionManager(models.Manager):
    def create(self, intern, project, commit=True):
        submission = Submission(submitter=intern, project=project)
        if commit:
            submission.save()
        return submission

class Submission(models.Model, model_permissions.IsAuth):
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='intern_submissions')
    project = models.ForeignKey(Project, related_name='submissions')
    status = models.IntegerField(choices = SubmissionStatus.CHOICES, default=SubmissionStatus.REGISTERED)

    objects = SubmissionManager()


    # ============== Write permissions

    # No writing directly to submissions
    @staticmethod
    def has_write_permission(request):
        return False


    # ============== Read permissions

    # Intern submitter and org project owner may read
    def has_object_read_permission(self, request):
        return (request.user == self.submitter) or (request.user == self.project.owner)


    # ============== Special action permissions

    # Intern submitter may submit
    @staticmethod
    def has_submit_permission(request):
        return model_permissions.checkAuth(request, user_type=UserTypes.INTERN, scopes=['write'])

    def has_object_submit_permission(self, request):
        return request.user == self.submitter


    # Org project owner may accept/reject
    @staticmethod
    def has_accept_permission(request):
        return model_permissions.checkAuth(request, user_type=UserTypes.ORG, scopes=['write'])

    def has_object_accept_permission(self, request):
        return request.user == self.project.owner

    @staticmethod
    def has_reject_permission(request):
        return model_permissions.checkAuth(request, user_type=UserTypes.ORG, scopes=['write'])

    def has_object_reject_permission(self, request):
        return request.user == self.project.owner


    # Submitter and owner may read files, write only for submitters handled in view
    @staticmethod
    def has_files_permission(request):
        return True

    def has_object_files_permission(self, request):
        return request.user == self.submitter or request.user == self.project.owner

    def __str__(self):
        return 'Submitter: %s | Project: %s' % (self.submitter, self.project)
