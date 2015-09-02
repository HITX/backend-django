from django.db import models
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Permission

from profiles.models import InternProfile, OrgProfile
from projects.models import Submission
from user_settings.models import UserSettings

from common.permissions import IsAuthOrReadOnlyAndCreate

from common.constants import UserTypes

class UserManager(BaseUserManager):
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})

        try:
            email = validated_data.pop('email')
            password = validated_data.pop('password')
        except KeyError as e:
            raise Exception(e.args[0] + ' missing from user create data')

        user = User(**validated_data)
        user.email = self.normalize_email(email)
        user.set_password(password)
        user.save(using=self._db)

        if user.is_intern:
            InternProfile.objects.create(user=user, **profile_data)
        elif user.is_org:
            OrgProfile.objects.create(user=user, **profile_data)
        else:
            raise Exception('Invalid user type')

        UserSettings.objects.create(user=user)

        return user

    def update(self, instance, validated_data):

        changed_fields = []

        profile_data = validated_data.pop('profile', {})
        email = validate_data.pop('email', None)
        password = validated_data.pop('password', None)

        if email:
            instance.email = self.normalize_email(email)
            changed_fields.append('email')
        if password:
            instance.set_password(password)
            changed_fields.append('password')
        for field, val in validated_data.items():
            instance[field] = val
            changed_fields.append(field)

        instance.save(using=self._db, update_fields=changed_fields)

        if instance.is_intern:
            InternProfile.objects.update(instance.profile, **profile_data)
        elif instance.is_org:
            OrgProfile.objects.update(instance.profile, **profile_data)
        else:
            raise Exception('Invalid user type')

        return instance

    # TODO: Get rid of create(...) and add validated_data to the
    # declaration in create_user and create_superuser
    def create_user(self, username, email, password=None):
        return self.create({
            'username': username,
            'email': email,
            'password': password,
            'user_type': UserTypes.INTERN
        })

    def create_superuser(self, username, email, password):
        user = self.create({
            'username': username,
            'email': email,
            'password': password,
            'user_type': UserTypes.INTERN,
            'is_staff': True
        })
        user.user_permissions = Permission.objects.all()
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
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'auth_user'

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    # def email_user(self, ...)


    # User type helpers
    def is_type(self, type):
        return self.user_type == type

    def _is_intern(self):
        # return self.user_type == self.USER_TYPE_INTERN
        return self.is_type(UserTypes.INTERN)

    def _is_org(self):
        # return self.user_type == self.USER_TYPE_ORG
        return self.is_type(UserTypes.ORG)

    is_intern = property(_is_intern)
    is_org = property(_is_org)


    # Profile helpers
    def _get_profile(self):
        # if self.user_type == self.USER_TYPE_INTERN:
        if self.is_intern:
            return self.intern_profile
        # elif self.user_type == self.USER_TYPE_ORG:
        elif self.is_org:
            return self.org_profile
        raise Exception('Unknown user type')

    profile = property(_get_profile)


    # Project helpers
    def _get_projects(self):
        if self.is_intern:
            return self.submitted_projects
        elif self.is_org:
            return self.owned_projects
        raise Exception('Unknown user type')

    projects = property(_get_projects)

    # Submission helpers
    def _get_submissions(self):
        if self.is_intern:
            return self.intern_submissions
        elif self.is_org:
            return Submission.objects.filter(project__owner=self)

        raise Exception('Unknown user type')

    submissions = property(_get_submissions)


    # Object permissions
    def has_object_read_permission(self, request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self
