# from django.contrib.auth import models
# from django.db.models import Manager
from profiles.models import Profile
from user_settings.models import UserSettings

from django.db import models
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def create(self, validated_data):

        profile_data = validated_data.pop('profile', {})

        try:
            username = validated_data.pop('username')
            email = validated_data.pop('email')
            password = validated_data.pop('password')
        except KeyError as e:
            raise ValueError('Users must have ' + e.args[0])

        user = User(**validated_data)
        user.username = username
        user.email = self.normalize_email(email)
        user.set_password(password)
        user.save(using=self._db)

        Profile.objects.create(user=user, **profile_data)
        UserSettings.objects.create(user=user)

        return user

    def create_user(self, username, email, password=None):
        return self.create({
            'username': username,
            'email': email,
            'password': password
        })

    def create_superuser(self, username, email, password):
        return self.create({
            'username': username,
            'email': email,
            'password': password,
            'is_staff': True
        })

        # user = self.create_user(username, email, password)
        #
        # user.is_staff = True
        # user.save(using=self._db)
        #
        # return user


class User(AbstractBaseUser, PermissionsMixin):
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

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'auth_user_new'

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    # def email_user(self, ...)

    @staticmethod
    def has_read_permission(request):
        return True

    @staticmethod
    def has_write_permission(request):
        user = request.user
        token = request.auth

        if (user and token and
            user.is_authenticated() and
            token.is_valid(['write'])):
            return True

        return False

    @staticmethod
    def has_create_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self



# class UserManager(models.UserManager):
#
#     def create(self, validated_data):
#         profile_data = validated_data.pop('profile', {})
#
#         # TODO: Properly validate that these fields exist before we get here
#         username = validated_data.pop('username')
#         email = validated_data.pop('email')
#         password = validated_data.pop('password')
#
#         user = self.create_user(username, email, password, **validated_data)
#
#         # user = User(**validated_data)
#         # user.save()
#
#         Profile.objects.create(user=user, **profile_data)
#         UserSettings.objects.create(user=user)
#
#         return user
#
#     # TODO: def update(self, instance, validated_data):
#
#
# class User(models.User):
#     objects = UserManager()
#
#     class Meta:
#         proxy = True
#
#     @staticmethod
#     def has_read_permission(request):
#         return True
#
#     @staticmethod
#     def has_write_permission(request):
#         user = request.user
#         token = request.auth
#
#         if (user and token and
#             user.is_authenticated() and
#             token.is_valid(['write'])):
#             return True
#
#         return False
#
#     @staticmethod
#     def has_create_permission(request):
#         return True
#
#     def has_object_read_permission(self, request):
#         return True
#
#     def has_object_write_permission(self, request):
#         return request.user == self
