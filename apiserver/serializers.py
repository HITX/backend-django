from django.contrib.auth.models import Group

from django.core.validators import RegexValidator

from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Field
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import NotFound

from apiserver.models import User
from apiserver.validators import RequiredValidator

from intern_profiles.models import InternProfile
from intern_profiles.serializers import InternProfileSerializer

from org_profiles.models import OrgProfile
from org_profiles.serializers import OrgProfileSerializer

from mixins.serializers import ErrorMessages

class BaseUserSerializer(ErrorMessages, ModelSerializer):
    # profile = ProfileField(required=False)

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
        extra_kwargs = {
            'password': {'write_only': True}
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


# TODO: Parameterize the serializer to use and pass it into the base's init

class InternSerializer(BaseUserSerializer):
    profile = InternProfileSerializer(required=False)

    class Meta(BaseUserSerializer.Meta):
        fields = ('profile',)

    def __init__(self, *args, **kwargs):
        self.Meta.fields += super(InternSerializer, self).Meta.fields
        super(InternSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        validated_data['user_type'] = User.USER_TYPE_INTERN
        return User.objects.create(validated_data)

    def update(self, instance, validated_data):
        if not instance.is_intern:
            raise NotFound

        return User.objects.update(instance, validated_data)


class OrgSerializer(BaseUserSerializer):
    profile = OrgProfileSerializer(required=False)

    class Meta(BaseUserSerializer.Meta):
        fields = ('profile',)

    def __init__(self, *args, **kwargs):
        self.Meta.fields += super(OrgSerializer, self).Meta.fields
        super(OrgSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        validated_data['user_type'] = User.USER_TYPE_ORG
        return User.objects.create(validated_data)

    def update(self, instance, validated_data):
        if not instance.is_org:
            raise NotFound

        return User.objects.update(instance, validated_data)

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
