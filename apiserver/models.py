from django.db import models
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Permission

from rest_framework.serializers import ValidationError

from profiles.models import InternProfile, OrgProfile
from user_settings.models import UserSettings
from submissions.models import Submission
from submission_files.models import SubmissionFile

from common.exceptions import InternalUserTypeError
from common.model_permissions import IsAuthOrReadOnlyAndCreate
from common.constants import UserTypes


class UserManager(BaseUserManager):
    def create(self, **validated_data):
        validated_profile_data = validated_data.pop('profile', {})

        try:
            email = validated_data.pop('email')
            password = validated_data.pop('password')
        except KeyError as e:
            raise ValidationError(e.args[0] + ' missing from user create data')

        user = User(**validated_data)
        user.email = self.normalize_email(email)
        user.set_password(password)
        user.save(using=self._db)

        if user.is_intern:
            InternProfile.objects.create(user=user, **validated_profile_data)
        elif user.is_org:
            OrgProfile.objects.create(user=user, **validated_profile_data)
        else:
            raise InternalUserTypeError

        # UserSettings.objects.create(user=user)

        return user

    # TODO: Add update method that overrides (behaves like) the normal
    # queryset update method. Must definitely use normalize_email and
    # set_password

    # def update(self, **validated_data):
    #     email = validated_data.pop('email', None)
    #     password = validated_data.pop('password', None)
    #     if email: validated_data.email = self.normalize_email(email)
    #     if password: validated_

    # def update(self, instance, **validated_data):
    #
    #     changed_fields = []
    #
    #     validated_profile_data = validated_data.pop('profile', None)
    #     email = validated_data.pop('email', None)
    #     password = validated_data.pop('password', None)
    #
    #     if email:
    #         instance.email = self.normalize_email(email)
    #         changed_fields.append('email')
    #     if password:
    #         instance.set_password(password)
    #         changed_fields.append('password')
    #     for field, val in validated_data.items():
    #         instance[field] = val
    #         changed_fields.append(field)
    #
    #     instance.save(using=self._db, update_fields=changed_fields)
    #     # instance.profile.update(**validated_profile_data)
    #
    #     if validated_profile_data:
    #         if instance.is_intern:
    #             InternProfile.objects.update(instance.profile, **validated_profile_data)
    #         elif instance.is_org:
    #             OrgProfile.objects.update(instance.profile, **validated_profile_data)
    #         else:
    #             raise InternalUserTypeError
    #
    #     return instance

    def create_user(self, username, email, password=None):
        return self.create(
            username = username,
            email = email,
            password = password,
            user_type = UserTypes.INTERN
        )

    def create_superuser(self, username, email, password):
        user = self.create(
            username = username,
            email = email,
            password = password,
            user_type = UserTypes.INTERN,
            is_staff = True
        )
        user.user_permissions = Permission.objects.all()
        user.save(using=self._db)
        return user


    # User type helpers
    def _get_interns(self):
        return self.get_queryset().filter(user_type=UserTypes.INTERN)

    def _get_orgs(self):
        return self.get_queryset().filter(user_type=UserTypes.ORG)

    interns = property(_get_interns)
    orgs = property(_get_orgs)


class User(AbstractBaseUser, PermissionsMixin, IsAuthOrReadOnlyAndCreate):
    username = models.CharField (
        max_length = 20,
        unique = True,
        help_text = 'Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only',
        validators = [
            validators.RegexValidator (
                r'^[\w.@+-]+$',
                'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters'
            )
        ],
        error_messages = {
            'unique': 'A user with that username already exists'
        }
    )
    email = models.EmailField (
        max_length = 255,
        verbose_name = 'email address',
        unique = True,
        error_messages = {
            'unique': 'A user with that email address already exists'
        }
    )
    is_staff = models.BooleanField (
        default = False,
        help_text = 'Designates whether the user can log into this admin site'
    )
    is_active = models.BooleanField (
        default = True,
        help_text = 'Designates whether this user should be treated as active. Unselect this instead of deleting accounts'
    )
    date_joined = models.DateTimeField( default = timezone.now )
    user_type = models.IntegerField( choices = UserTypes.CHOICES )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['_email']

    class Meta:
        db_table = 'auth_user'

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    # def email_user(self, ...)

    # Special email setter
    def set_email(self, val):
        self.email = self.objects.normalize_email(val)

    # User type helpers
    def is_type(self, type):
        return self.user_type == type
    def _is_intern(self):
        return self.is_type(UserTypes.INTERN)
    def _is_org(self):
        return self.is_type(UserTypes.ORG)
    is_intern = property(_is_intern)
    is_org = property(_is_org)

    # Profile helpers
    def _get_profile(self):
        if self.is_intern:
            return self.intern_profile
        elif self.is_org:
            return self.org_profile
        raise Exception('Unknown user type')
    profile = property(_get_profile)

    # Project helpers
    def _get_projects(self):
        if self.is_intern:
            return self.submitted_projects.get_queryset()
        elif self.is_org:
            return self.owned_projects.get_queryset()
        raise Exception('Unknown user type')
    projects = property(_get_projects)

    # Submission helpers
    def _get_submissions(self):
        if self.is_intern:
            return self.intern_submissions.get_queryset()
        elif self.is_org:
            return Submission.objects.filter(project__owner=self)
        raise Exception('Unknown user type')
    submissions = property(_get_submissions)

    # Submission file helpers
    def _get_submission_files(self):
        if self.is_intern:
            return self.submitted_files.get_queryset()
        elif self.is_org:
            return SubmissionFile.objects.filter(submission__project__owner=self)
        raise Exception('Unknown user type')
    submission_files = property(_get_submission_files)


    # Object permissions
    def has_object_read_permission(self, request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self
