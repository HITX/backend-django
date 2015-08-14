from django.contrib.auth import models
from django.db.models import Manager
from profiles.models import Profile

class UserManager(Manager):

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        user = User(**validated_data)
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user

    # TODO: def update(self, instance, validated_data):

class User(models.User):
    objects = UserManager()

    class Meta:
        proxy = True

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
