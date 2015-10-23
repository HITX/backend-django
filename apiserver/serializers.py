from django.contrib.auth.models import Group

from django.core.validators import RegexValidator

# from rest_framework.serializers import Serializer, ModelSerializer, CharField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import NotFound

from common.constants import UserTypes

from apiserver.models import User

from profiles.models import InternProfile, OrgProfile
from profiles.serializers import InternProfileSerializer, OrgProfileSerializer

from common.serializers import ErrorMessagesMixin, DynamicModelSerializer

from abc import ABCMeta, abstractmethod

# TODO: remove this
from rest_framework.serializers import ValidationError


class BaseUserSerializer(ErrorMessagesMixin, DynamicModelSerializer):
    class Meta:
        abstract = True
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
            'user_type',
        )
        read_only_fields = ('user_type',)
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }
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

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    password_check = serializers.CharField()

    def validate(self, data):
        # raise ValidationError('Serializer validate breakpoint')
        user = self.context['request'].user
        print 'serializer user:'
        print user
        password_check = data['password_check']
        if not user.check_password(password_check):
            raise ValidationError({'password_check': 'Invalid password'})

        return data

# class TestInternAbstract(object):
#     __metaclass__ = ABCMeta
#
#     @abstractmethod
#     def get_profile_serializer(): pass
#
#     def __init__(self, *args, **kwargs):
#         profile_serializer_class = get_profile_serializer()
#         self.fields['profile'] = profile_serializer_(class(required=False)
#         self.Meta.fileds += ('profile',)
#         self.profile_fields = profile_serializer_class.Meta.fields
#         super(TestInternAbstract, self).__init__(*args, **kwargs)


class TestInternSerializer(BaseUserSerializer):

    profile = InternProfileSerializer(required=False)

    def __init__(self, *args, **kwargs):
        self.Meta.fields += ('profile',)
        self.profile_fields = InternProfileSerializer.Meta.fields
        super(TestInternSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, instance):
        res = super(TestInternSerializer, self).to_representation(instance)
        tmp = res.pop('profile')
        res.update(tmp)
        return res

    def to_internal_value(self, data):
        # Disallow direct setting of profile
        data.pop('profile', None)

        profile_data = {}
        for field_name in self.profile_fields:
            field_data = data.pop(field_name, None)
            if field_data:
                profile_data[field_name] = field_data

        if profile_data:
            data['profile'] = profile_data

        return super(TestInternSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        validated_data['user_type'] = UserTypes.INTERN
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        raise ValidationError('Use special endpoints to update username/email/password')

        # validated_profile_data = validated_data.pop('profile', None)
        #
        # email = validated_data.pop('email', None)
        # password = validated_data.pop('password', None)
        #
        # if email: instance.set_email(email)
        # if password: instance.set_password(password)
        # for field, val in validated_data.items():
        #     setattr(instance, field, val)
        # instance.save()
        #
        # if validated_profile_data:
        #     profile = instance.profile
        #     for field, val in validated_profile_data.items():
        #         setattr(profile, field, val)
        #     profile.save()
        #
        # return instance


# TODO: Parameterize the serializer to use and pass it into the base's init

class InternSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        inline_fields = {'profile': InternProfileSerializer}

    def create(self, validated_data):
        validated_data['user_type'] = UserTypes.INTERN
        return User.objects.create(validated_data)

    def update(self, instance, validated_data):
        if not instance.is_intern:
            # TODO: change to custom invalid user type exception
            raise NotFound
        return User.objects.update(instance, validated_data)


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
