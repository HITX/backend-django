from django.contrib.auth.models import Group

from django.core.validators import RegexValidator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import NotFound

from common.constants import UserTypes

from apiserver.models import User

from profiles.models import InternProfile, OrgProfile
from profiles.serializers import InternProfileSerializer, OrgProfileSerializer

from common.serializers import ErrorMessagesMixin, DynamicModelSerializer


class BaseUserSerializer(ErrorMessagesMixin, DynamicModelSerializer):
    password_check = serializers.CharField(required=False)

    class Meta:
        abstract = True
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
            'user_type',
            'password_check'
        )
        read_only_fields = ('user_type',)
        extra_kwargs = {
            'password': {'write_only': True},
            'password_check': {'write_only': True}
        }
        error_messages = {
            'username': {
                'names': { 'required': 'Username is required' },
                'validators': {
                    UniqueValidator: 'A user with that username already exists',
                    RegexValidator: 'Invalid username'
                }
            },
            'email': {
                'names': { 'required': 'Email is required' },
                'validators': { UniqueValidator: 'A user with that email already exists' }
            },
            'password': {
                'names': { 'required': 'Password is required' }
            }
        }

    # TODO: add update override here that correctly sets email and password

class InternSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        inline_fields = {'profile': InternProfileSerializer}

    def create(self, validated_data):
        profile_data = {}
        for field_name in self.inline_fields['profile']:
            field_data = validated_data.pop(field_name, None)
            if field_data:
                profile_data[field_name] = field_data

        if profile_data:
            validated_data['profile'] = profile_data

        validated_data['user_type'] = UserTypes.INTERN
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        if profile_data:
            profile = self.context['request'].user.profile
            InternProfile.objects.filter(pk=profile.pk).update(**profile_data)

        return super(InternSerializer, self).update(instance, validated_data)


class OrgSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        inline_fields = {'profile': OrgProfileSerializer}

    def create(self, validated_data):
        validated_data['user_type'] = UserTypes.ORG
        return User.objects.create(validated_data)

    def update(self, instance, validated_data):
        if not instance.is_org:
            # TODO: change to custom invalid user type exception
            raise NotFound
        return User.objects.update(instance, validated_data)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
