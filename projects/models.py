from django.db import models
from django.conf import settings

from constants import UserTypes, SubmissionStatus

from mixins.models import permissions

class Project(models.Model, permissions.IsAuthOrReadOnly):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_projects')
    submitters = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Submission', related_name='submitted_projects')
    title = models.CharField(max_length=256, default='Project Title')
    description = models.TextField(max_length=1024, default='Project description and so on...')


    # Class permissions
    @staticmethod
    def has_create_permission(request):
        return permissions.checkAuth(request, user_type=UserTypes.ORG, scopes=['write'])

    @staticmethod
    def has_register_permission(request):
        return permissions.checkAuth(request, user_type=UserTypes.INTERN, scopes=['write'])

    # Object permissions
    def has_object_read_permission(self, request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.owner

    def has_object_register_permission(self, request):
        return True

    def __str__(self):
        return self.title

class SubmissionManager(models.Manager):
    def create(self, intern, project, commit=True):
        submission = Submission(submitter=intern, project=project)
        if commit:
            submission.save()
        return submission

class Submission(models.Model, permissions.IsAuth):
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='intern_submissions')
    project = models.ForeignKey(Project, related_name='submissions')
    status = models.IntegerField(choices = SubmissionStatus.CHOICES, default=SubmissionStatus.REGISTERED)

    objects = SubmissionManager()

    @staticmethod
    def has_write_permission(request):
        return False

    @staticmethod
    def has_submit_permission(request):
        return permissions.checkAuth(request, user_type=UserTypes.INTERN, scopes=['write'])

    @staticmethod
    def has_accept_permission(request):
        return permissions.checkAuth(request, user_type=UserTypes.ORG, scopes=['write'])

    @staticmethod
    def has_reject_permission(request):
        return permissions.checkAuth(request, user_type=UserTypes.ORG, scopes=['write'])

    # TODO: don't forget delete permissions

    # Object permissions
    def has_object_read_permission(self, request):
        return (request.user == self.submitter) or (request.user == self.project.owner)

    def has_object_write_permission(self, request):
        return False

    def has_object_submit_permission(self, request):
        return request.user == self.submitter

    def has_object_accept_permission(self, request):
        return request.user == self.project.owner

    def has_object_reject_permission(self, request):
        return request.user == self.project.owner

    def __str__(self):
        return 'Submitter: %s | Project: %s' % (self.submitter, self.project)
